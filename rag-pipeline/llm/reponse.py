from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def generate_reponse_rag(llm, prompt_content, retriever, user_prompt):

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


def generate_response_llm(llm, prompt_content, user_prompt):
    try:
        prompt_template = PromptTemplate.from_template(prompt_content)
        model = prompt_template | llm
        result = model.invoke({"question": user_prompt})
    except:
        result = llm.invoke({"question": user_prompt})
    # return result
    return result
