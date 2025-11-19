import base64
import json
import datetime

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        try:
            # 1. Decodificar o payload que vem em Base64
            payload = base64.b64decode(record['data']).decode('utf-8')
            data_json = json.loads(payload)
            
            # Exemplo: Adicionando data de processamento
            data_json['processed_at'] = datetime.datetime.now().isoformat()
                
            # Exemplo: Adicionando uma tag de curso
            data_json['course_module'] = 'AWS Data Streaming'
            
            # 2. Preparar o dado para devolução (JSON -> String + \n)
            output_payload = json.dumps(data_json) + "\n"
            
            # 3. Codificar de volta para Base64
            output_base64 = base64.b64encode(output_payload.encode('utf-8')).decode('utf-8')

            # 4. Montar o objeto de resposta exigido pelo Firehose
            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok', # Indica sucesso.
                'data': output_base64
            }
            output.append(output_record)

        except Exception as e:
            print(f"Falha ao processar registro {record['recordId']}: {e}")
            # Em caso de erro de parse, marcamos como falha
            output_record = {
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data'] # Devolvemos o dado original
            }
            output.append(output_record)

    print(f"Processados {len(output)} registros com sucesso.")
    return {'records': output}