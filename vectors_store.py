from langchain_chroma import Chroma
import config_data as config




class VectorstoreService(object):
    def __init__(self,embedding):
        self.embedding=embedding
        self.vector_store=Chroma(

            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriver(self):
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})

if __name__=='__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever=VectorstoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriver()
    res=retriever.invoke("吕行嘉是谁")
    print(res)
