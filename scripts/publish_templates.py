"""Publish only the authored notebooks and static outputs to a specified public project."""
import argparse,json
from pathlib import Path
import wandb
p=argparse.ArgumentParser();p.add_argument('--project',required=True);a=p.parse_args();entity,project=a.project.split('/')
api=wandb.Api();query=api._service_api.execute_graphql
receipt=Path('evidence/hosted-templates.json');saved=json.loads(receipt.read_text()) if receipt.exists() else {}
for slug,title in [('starter','Forge Workshop Kit · Starter'),('facilitator','Forge Workshop Kit · Progress monitor'),('pending_inc','Pending, Inc. · Your project'),('solar_autoresearch','Build a research loop, then give it an agent')]:
 source=Path('notebooks')/(slug+'.py');html=Path('dist')/(slug+'.html');assert source.exists() and html.exists()
 if slug not in saved:
  created=query('mutation($e:String!,$p:String!){createNotebook(input:{entityName:$e,projectName:$p,template:BASIC}){notebook{id name}}}',{'e':entity,'p':project})['createNotebook']['notebook']
  saved[slug]={'id':created['id']};receipt.write_text(json.dumps(saved,indent=2))
 nb=query('mutation($id:ID!,$n:String!){renameNotebook(input:{id:$id,name:$n}){notebook{id name currentVersion{artifactCollectionName versionIndex} viewerPermissions}}}',{'id':saved[slug]['id'],'n':title})['renameNotebook']['notebook']
 with wandb.init(entity=entity,project=project,job_type='workshop-template',name=title,settings=wandb.Settings(disable_git=True)) as run:
  artifact=wandb.Artifact(nb['currentVersion']['artifactCollectionName'],type='notebook',metadata={'release':'0.2.3','public_teaching_material':True,'gateway':False})
  artifact.add_file(str(source),name='notebook.py');artifact.add_file(str(html),name='__marimo__/notebook.html');run.log_artifact(artifact).wait()
 read=query('query($id:ID!){notebook(id:$id){id name currentVersion{artifactCollectionName versionIndex sourceFileName} viewerPermissions}}',{'id':nb['id']})['notebook']
 assert read['currentVersion']['versionIndex']==int(artifact.version[1:])
 saved[slug]={**read,'url':f"https://forge.coreweave.com/notebooks/{nb['id']}/view",'edit_url':f"https://forge.coreweave.com/notebooks/{nb['id']}"}
 receipt.write_text(json.dumps(saved,indent=2));print(slug,saved[slug]['url'],flush=True)
