import json
import boto3
import os
import uuid

# boto3 -> SDK da Amazon para Python
# https://pypi.org/project/boto3/
# Coleta as informações do serviço 's3' presentes nessa conta
s3 = boto3.client('s3')
# Coleta a variável de ambiente 'BUCKET_NAME'
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Coleta o 'body' da requisição, que é o conteúdo a ser postado
        body = json.loads(event.get('body', '{}'))
        
        # Gera um nome único aleatório
        # IMPORTANTE: nomes de arquivos e do bucket devem ser únicos!
        file_name = f"{uuid.uuid4()}.json"
        
        # Faz o upload para o S3
        # Parâmetros: nome do bucket, nome do arquivo, conteúdo do arquivo (body)
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(body),
            ContentType='application/json'
        )
        
        # Retorna o nome do arquivo salvo
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Data saved successfully", "file": file_name})
        }
    # Caso dê problema, captura o erro
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }