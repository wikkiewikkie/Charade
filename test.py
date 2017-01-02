import charade

if __name__ == "__main__":

    c = charade.Charade(size=100)

    for doc in c:
        print(type(doc), doc.document_id, len(doc))
        for attachment in doc:
            print("\t", type(attachment), attachment.document_id, len(attachment))
