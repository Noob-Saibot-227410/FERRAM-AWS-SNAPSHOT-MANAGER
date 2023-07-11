from flask import Flask, render_template
import boto3

# Cria uma instância da classe Flask, definindo o nome do módulo (__name__) e o diretório dos templates
app = Flask(__name__, template_folder='templates')

# Define a rota raiz do aplicativo Flask
@app.route('/')
def index():
    ec2 = boto3.resource('ec2')  # Cria um objeto resource para interagir com o serviço EC2 da AWS
    snapshots = ec2.snapshots.all()  # Obtém todos os snapshots do EC2
    return render_template('index.html', snapshots=snapshots)  # Renderiza o template HTML passando os snapshots como contexto

# Define a rota para a página RDS
@app.route('/rds')
def rds():
    session = boto3.Session(profile_name='default')  # Cria uma sessão utilizando o profile 'default' do arquivo de credenciais
    rds = session.client('rds')  # Cria um objeto client para interagir com o serviço RDS da AWS
    try:
        snapshots = rds.describe_db_snapshots()['DBSnapshots']  # Obtém todos os snapshots do RDS
    except Exception as e:
        print("Erro ao obter snapshots do RDS:", str(e))
        snapshots = []
    return render_template('rds.html', snapshots=snapshots)  # Renderiza o template HTML passando os snapshots como contexto

# Define a rota para a página S3
@app.route('/s3')
def s3():
    session = boto3.Session(profile_name='default')  # Cria uma sessão utilizando o profile 'default' do arquivo de credenciais
    s3 = session.client('s3')  # Cria um objeto client para interagir com o serviço S3 da AWS
    try:
        response = s3.list_buckets()  # Obtém a lista de buckets do S3
        buckets = response['Buckets']
        snapshots = []
        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket_snapshots = s3.list_object_versions(Bucket=bucket_name)['Versions']
            snapshots.extend(bucket_snapshots)
    except Exception as e:
        print("Erro ao obter snapshots do S3:", str(e))
        snapshots = []
    return render_template('s3.html', snapshots=snapshots)  # Renderiza o template HTML passando os snapshots como contexto

# Define a rota para a página EBS
@app.route('/ebs')
def ebs():
    session = boto3.Session(profile_name='default')  # Cria uma sessão utilizando o profile 'default' do arquivo de credenciais
    ec2 = session.client('ec2')  # Cria um objeto client para interagir com o serviço EC2 da AWS
    try:
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']  # Obtém todos os snapshots do EBS
    except Exception as e:
        print("Erro ao obter snapshots do EBS:", str(e))
        snapshots = []
    return render_template('ebs.html', snapshots=snapshots)  # Renderiza o template HTML passando os snapshots como contexto

# Define a rota para recursos não encontrados
@app.route('/none')
def none():
    return render_template('none.html')

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor de desenvolvimento do Flask com a opção de depuração ativada