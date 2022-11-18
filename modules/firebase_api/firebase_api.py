import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Firebase_API(metaclass=SingletonMeta):
    def __init__(self, Accountkey, storagebucket):
        cred = credentials.Certificate(Accountkey)
        firebase_admin.initialize_app(cred, {'storageBucket' : storagebucket})
        self.db = firestore.client()
        self.bucket = storage.bucket()


    def Add_document(self, data, collection, document, merged):
        #true for change documents and False for add docmunets
        self.db.collection(collection).document(document).set(data, merged)
        pass

    def Uploadimage(self, filepath):
        print(filepath)
        blob = self.bucket.blob(filepath)
        blob.upload_from_filename(filepath)
        blob.make_public()
        return blob.public_url