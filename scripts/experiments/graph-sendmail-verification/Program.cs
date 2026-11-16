using System.Net;
using System.Text;
using System.Text.Json;
using Microsoft.Graph;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Graph.Models;
using Microsoft.Graph.Users.Item.SendMail;
using Microsoft.Kiota.Http.HttpClientLibrary.Middleware;
using Microsoft.Kiota.Http.HttpClientLibrary.Middleware.Options;
using Microsoft.Kiota.Serialization.Json;

// Validate the real article's request payload without sending any email.
var body = CreateSample("ORDER-123", "test@example.invalid");
using (var writer = new JsonSerializationWriter())
{
    writer.WriteObjectValue(null, body);
    using var stream = writer.GetSerializedContent();
    using var json = JsonDocument.Parse(stream);
    var root = json.RootElement;
    Console.WriteLine("Serialized request: " + root.GetRawText());
    Require(GetIgnoreCase(root, "saveToSentItems").GetBoolean(), "saveToSentItems should serialize as true");
    Require(GetIgnoreCase(GetIgnoreCase(root, "message"), "subject").GetString() == "Order ORDER-123 confirmed",
        "Message subject was not serialized");
    Console.WriteLine("PASS: Graph 6.10.0 sendMail serialization");
}

// Test the Kiota retry middleware with deterministic HTTP stubs, never live endpoints.
// The no-retry handler must not repeat requests even if the response is normally retryable.
foreach (var status in new[] { HttpStatusCode.TooManyRequests, HttpStatusCode.ServiceUnavailable })
{
    var stub = new CountingHandler(status);
    using var handler = new RetryHandler(new RetryHandlerOption { MaxRetry = 0 })
    {
        InnerHandler = stub
    };
    using var client = new HttpClient(handler);
    using var request = new HttpRequestMessage(HttpMethod.Post, "https://graph.microsoft.com/v1.0/users/test/sendMail")
    {
        Content = new StringContent("{}", Encoding.UTF8, "application/json")
    };
    using var response = await client.SendAsync(request);
    Require(response.StatusCode == status, $"Expected {status} response");
    Require(stub.Count == 1, $"Expected exactly one outbound request for {status}; got {stub.Count}");
    Console.WriteLine($"PASS: MaxRetry=0 on {(int)status} => one outbound attempt");
}

// Exercise the article's EF Core snippet with a real SQLite transaction, not mocks.
using (var connection = new SqliteConnection("Data Source=:memory:"))
{
    await connection.OpenAsync();
    var options = new DbContextOptionsBuilder<ArticleDb>().UseSqlite(connection).Options;
    await using var db = new ArticleDb(options);
    await db.Database.EnsureCreatedAsync();

    var order = new OrderRecord();
    db.Orders.Add(order);
    db.NotificationOutbox.Add(new NotificationOutboxMessage
    {
        Order = order,
        Status = "Pending"
    });
    await db.SaveChangesAsync(CancellationToken.None);

    Require(order.Id > 0, "Database-generated order ID was not assigned");
    Require(await db.Orders.CountAsync() == 1 && await db.NotificationOutbox.CountAsync() == 1,
        "Order and outbox were not committed together");
    Console.WriteLine("PASS: EF Core order + outbox inserted in one SaveChangesAsync");

    // A failed dependent insert must roll back the parent insert.
    var rejectedOrder = new OrderRecord();
    db.Orders.Add(rejectedOrder);
    db.NotificationOutbox.Add(new NotificationOutboxMessage
    {
        Order = rejectedOrder,
        Status = null! // Violates the non-null SQLite column constraint.
    });

    try
    {
        await db.SaveChangesAsync(CancellationToken.None);
        throw new InvalidOperationException("Expected SQLite to reject a null outbox status");
    }
    catch (DbUpdateException)
    {
        db.ChangeTracker.Clear();
    }

    Require(await db.Orders.CountAsync() == 1 && await db.NotificationOutbox.CountAsync() == 1,
        "Failed SaveChangesAsync must not commit an orphaned order");
    Console.WriteLine("PASS: EF Core transaction rolled back after failed outbox insert");
}

// Verify compilation of the SDK request-builder call without sending live email.
_ = (Func<GraphServiceClient, string, string, string, CancellationToken, Task>)SdkSendMailExample;
static async Task SdkSendMailExample(
    GraphServiceClient graphClient, string senderUserId,
    string orderNumber, string customerEmail,
    CancellationToken cancellationToken)
{
    var request = CreateSample(orderNumber, customerEmail);
    await graphClient.Users[senderUserId]
        .SendMail
        .PostAsync(request, cancellationToken: cancellationToken);
}

static SendMailPostRequestBody CreateSample(string orderNumber, string customerEmail) => new()
{
    Message = new Message
    {
        Subject = $"Order {orderNumber} confirmed",
        Body = new ItemBody
        {
            ContentType = BodyType.Text,
            Content = "Your order has been accepted."
        },
        ToRecipients = new List<Recipient>
        {
            new()
            {
                EmailAddress = new EmailAddress
                {
                    Address = customerEmail
                }
            }
        }
    },
    SaveToSentItems = true
};

static JsonElement GetIgnoreCase(JsonElement obj, string name)
{
    foreach (var property in obj.EnumerateObject())
    {
        if (string.Equals(property.Name, name, StringComparison.OrdinalIgnoreCase))
            return property.Value;
    }
    throw new InvalidOperationException($"Missing serialized property: {name}");
}

static void Require(bool condition, string reason)
{
    if (!condition) throw new InvalidOperationException(reason);
}

sealed class CountingHandler(HttpStatusCode status) : HttpMessageHandler
{
    public int Count { get; private set; }
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        Count++;
        return Task.FromResult(new HttpResponseMessage(status) { RequestMessage = request });
    }
}

sealed class ArticleDb(DbContextOptions<ArticleDb> options) : DbContext(options)
{
    public DbSet<OrderRecord> Orders => Set<OrderRecord>();
    public DbSet<NotificationOutboxMessage> NotificationOutbox => Set<NotificationOutboxMessage>();
}

sealed class OrderRecord
{
    public int Id { get; set; }
}

sealed class NotificationOutboxMessage
{
    public int Id { get; set; }
    public OrderRecord Order { get; set; } = null!;
    public string Status { get; set; } = "";
}
