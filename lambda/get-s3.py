import json
import boto3
import os

# boto3 -> SDK da Amazon para Python
# https://pypi.org/project/boto3/
# Coleta as informações do serviço 's3' presentes nessa conta
s3 = boto3.client('s3')
# Coleta a variável de ambiente 'BUCKET_NAME'
BUCKET_NAME = os.environ.get('BUCKET_NAME')  # Same bucket as above

def lambda_handler(event, context):
    try:
        # Lista todos os objetos presentes no bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        # Tratamento de erro caso não hajam arquivos no bucket
        if 'Contents' not in response:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Bucket está vazio!"})
            }
        
        all_files_data = {}
        
        # Itera sobre cada arquivo e retorna seu conteúdo
        for obj in response['Contents']:
            key = obj['Key']
            file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            content = file_obj['Body'].read().decode('utf-8')
            
            # Guarda o conteúdo de cada arquivo separando pelo seu respectivo nome
            all_files_data[key] = json.loads(content) if content.strip().startswith('{') else content
        
        return {
            "statusCode": 200,
            "body": json.dumps(all_files_data, indent=2)
        }
    # Caso dê problema, captura o erro
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
