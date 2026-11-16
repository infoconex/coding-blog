using System.Net;
using System.Text;
using System.Text.Json;
using Microsoft.Graph;
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
    Require(root.GetProperty("saveToSentItems").GetBoolean(), "saveToSentItems should serialize as true");
    Require(root.GetProperty("message").GetProperty("subject").GetString() == "Order ORDER-123 confirmed",
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

// The snippet is compiled against the pinned package; it deliberately is not invoked.
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
