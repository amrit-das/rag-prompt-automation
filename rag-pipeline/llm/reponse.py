from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def generate_reponse(llm, prompt_content, retriever, user_prompt):

    prompt_template = PromptTemplate(
        template=prompt_content, input_variables=["context", "question"]
    )
    llm_init = RetrievalQA.from_llm(
        llm=llm,
        prompt=prompt_template,
        retriever=retriever,
        return_source_documents=True,
    )

    results = llm_init({"querry": user_prompt})
    return results
