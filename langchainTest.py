import langchain
from langchain import PromptTemplate, LLMChain
from langchain.llms import TextGen

model_url = "http://localhost:5000"
langchain.debug = True

template = """Question: {question}

Answer: Let's think step by step."""


prompt = PromptTemplate(template=template, input_variables=["question"])
llm = TextGen(model_url=model_url)
llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
llm_chain.run(question)