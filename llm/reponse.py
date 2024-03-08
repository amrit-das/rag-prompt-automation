from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def generate_response_rag(llm, prompt_content, retriever, question):

    prompt_template = PromptTemplate(
        template=prompt_content, input_variables=["context", "question"]
    )
    llm_init = RetrievalQA.from_llm(
        llm=llm,
        prompt=prompt_template,
        retriever=retriever,
        return_source_documents=True,
    )

    results = llm_init({"query": question})
    return results


def generate_response_llm(llm, prompt_content, user_prompt):
    try:
        prompt_template = PromptTemplate.from_template(prompt_content)
        model = prompt_template | llm
        result = model.invoke({"user_prompt": user_prompt})
    except Exception as e:
        print(e)
        result = llm.invoke({"user_prompt": user_prompt})
    return result
