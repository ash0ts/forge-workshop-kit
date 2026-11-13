import argparse
import wandb
parser=argparse.ArgumentParser()
parser.add_argument('project')
args=parser.parse_args()
entity,project=args.project.split('/')
api=wandb.Api()
api.create_project(project,entity)
result=api._service_api.execute_graphql('mutation($e:String!,$p:String!){upsertModel(input:{entityName:$e,name:$p,access:"USER_READ"}){project{name}}}',{'e':entity,'p':project})
print(result)
