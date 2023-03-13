from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    ec2 = boto3.resource('ec2')
    snapshots = ec2.snapshots.all()
    return render_template('index.html', snapshots=snapshots)

@app.route('/copy-snapshot/<snapshot_id>')
def copy_snapshot(snapshot_id):
    ec2 = boto3.client('ec2')
    snapshot = ec2.describe_snapshots(SnapshotIds=[snapshot_id])['Snapshots'][0]
    snapshot_name = snapshot['Description'] + ' - copy'
    new_snapshot = ec2.copy_snapshot(SourceSnapshotId=snapshot_id, Description=snapshot_name)
    return redirect(url_for('index'))

@app.route('/rename-snapshot/<snapshot_id>', methods=['POST'])
def rename_snapshot(snapshot_id):
    ec2 = boto3.client('ec2')
    snapshot = ec2.describe_snapshots(SnapshotIds=[snapshot_id])['Snapshots'][0]
    new_description = request.form['new_description']
    ec2.modify_snapshot_attribute(SnapshotId=snapshot_id, Attribute='description', Value=new_description)
    return redirect(url_for('index'))

@app.route('/delete-snapshot/<snapshot_id>')
def delete_snapshot(snapshot_id):
    ec2 = boto3.client('ec2')
    ec2.delete_snapshot(SnapshotId=snapshot_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
