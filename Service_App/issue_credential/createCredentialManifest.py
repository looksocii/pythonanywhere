from Service_App.issue_credential.createCredential import create_credential
from Service_App.issue_credential.createManifest import Manifest, AggregateCredential

def create():
   create_credential()
   
   manifest = Manifest()
   manifest.create()

   aggregateCredential = AggregateCredential()
   aggregateCredential.addProof2manifest()

if __name__ == '__main__':
    create()