
const repo="infoconex/coding-blog",ref="756d345c9996dd1a778ae4e85f26df4349147c6c";
const rr=await Promise.all(years.map(y=>tools.mcp__GitHub__search({query:"/post/"+y+"/",repository_name:repo,topn:100})));
const all=[...new Set(rr.flatMap(r=>r.result.results.map(x=>x.path).filter(p=>/^post\/\d{4}\/\d\d\/\d\d\/.+\/index\.md$/.test(p))))].sort();
const paths=all.slice(start,start+take);
const docs=await Promise.allSettled(paths.map(path=>tools.mcp__GitHub__fetch_file({repository_full_name:repo,path,ref})));
const loc="scripts/reports/seo-aeo-article-baseline-2026-10-28.csv";
const report=(await tools.mcp__GitHub__fetch_file({repository_full_name:repo,path:loc,ref:"main"})).result;
const q=v=>'"'+String(v??"").replace(/"/g,'""').replace(/[\r\n]+/g," ")+'"';
const found=[];
for(let i=0;i<paths.length;i++){
 if(docs[i].status!=="fulfilled")continue;
 const f=docs[i].value.result,front=f.content.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
 if(!front)continue;
 const d={},b=f.content.slice(front[0].length);let k="";
 for(const ln of front[1].split(/\r?\n/)){
  const m=ln.match(/^(\w+):\s*(.*)$/);
  if(m){k=m[1];const v=m[2].trim();d[k]=v==="[]" ? []:v.startsWith("[")&&v.endsWith("]") ? v.slice(1,-1).split(",").map(x=>x.trim().replace(/^["']|["']$/g,"")).filter(Boolean):v.replace(/^["']|["']$/g,"");}
  else if(/^\s+-\s+/.test(ln)){if(!Array.isArray(d[k]))d[k]=[];d[k].push(ln.replace(/^\s+-\s+/,"").replace(/^["']|["']$/g,""));}
 }
 if(d.published==="false")continue;
 const noCode=b.replace(/^\s*```[^\n]*\n[\s\S]*?^\s*```\s*$/gm," ");
 const wc=(noCode.match(/[\p{L}\p{N}][\p{L}\p{N}'’-]*/gu)||[]).length;
 const h1=(noCode.match(/^#\s+|<h1(?:\s|>)/gmi)||[]).length,h2=(noCode.match(/^##\s+|<h2(?:\s|>)/gmi)||[]).length;
 const alt=[...b.matchAll(/!\[([^\]]*)\]\([^)]+\)/g)].filter(x=>!x[1].trim()).length+[...b.matchAll(/<img\b[^>]*>/gi)].filter(x=>!/\balt\s*=/i.test(x[0])).length;
 const fence=[...b.matchAll(/^\s*```([^\n`]*)/gm)].filter((x,j)=>j%2===0&&!x[1].trim()).length;
 const links=new Set([...b.matchAll(/\]\((?:https?:\/\/coding\.infoconex\.com)?(\/post\/[^)\s]+)/gi)].map(x=>x[1])).size;
 const ext=[...new Set([...b.matchAll(/https?:\/\/[^\s"'<>)}\]]+/g)].map(x=>x[0]).filter(x=>!x.includes("coding.infoconex.com")))];
 const http=ext.filter(x=>x.startsWith("http://")).length,old=ext.filter(x=>/infoconex\.github\.io|ai-flywheel\.infoconex\.com/i.test(x)).length;
 const title=d.title||"",description=d.description||"",tags=Array.isArray(d.tags)?d.tags:[],technical=/\.net|c#|asp\.net|software|design|linux|security|GitHub|SDK|architecture|server|windows|api|LINQ|Azure|SSL|WCF|DNS|traceroute|GZip|BlueQuartz/i.test(title);
 const seo=[],aeo=[],acc=[],link=[],refs=[];
 if(!description)seo.push("Missing description");else if(description.length<85||description.length>190||/[…]\s*$/.test(description))seo.push("Review description");
 if(!tags.length)seo.push("Missing topic tags");
 if(title.length<22||title.length>85)seo.push("Review title length");
 if(h1)acc.push("H1 duplicates layout H1");
 if(alt)acc.push(alt+" missing alt");
 if(fence)acc.push(fence+" unlabelled code");
 if(wc>300&&h2===0)aeo.push("Improve article section headings");
 if(technical&&wc>250&&links===0)link.push("Review contextual links");
 if(http)refs.push(http+" HTTP URLs to verify");
 if(old)refs.push(old+" old project URLs to verify");
 if(/https?:\/\/(?:msdn\.microsoft\.com|blogs\.msdn\.com)/i.test(b))refs.push("Review legacy Microsoft docs");
 const rec=[...seo,...aeo,...acc,...link,...refs].join("; ");
 const score=(h1?4:0)+(alt?4:0)+(fence?3:0)+(!tags.length?3:0)+(!description?4:seo.includes("Review description")?2:0)+(wc>300&&h2===0?4:0)+(link.length?2:0)+(old?3:0)+(http?1:0)+(technical?1:0);
 const pri=score>=9?"High":score>=5?"Medium":"Low";
 found.push({row:[title,d.date,"https://coding.infoconex.com"+d.permalink,paths[i],wc,seo.join("; "),aeo.join("; "),acc.join("; "),link.join("; "),refs.join("; "),rec,pri,tags.join("; "),h1,h2,alt,fence,links,ext.length,description.length,f.sha].map(q).join(","),title,priority:pri,score,issues:rec.slice(0,160)});
}
const next=report.content.trimEnd()+"\r\n"+found.map(x=>x.row).join("\r\n")+"\r\n";
const saved=await tools.mcp__GitHub__update_file({repository_full_name:repo,path:loc,sha:report.sha,content:next,message:"Extend 2026 article audit baseline: "+years.join("-")+" ("+start+"-"+(start+take)+")",branch:"main"});
return {years,start,identified:all.length,scanned:paths.length,added:found.length,commit:saved.result.commit_sha,top:found.sort((a,b)=>b.score-a.score).slice(0,5).map(x=>({title:x.title,priority:x.priority,score:x.score,issues:x.issues}))};
