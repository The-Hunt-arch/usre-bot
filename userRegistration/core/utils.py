from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
import os

os.environ["AZURE_OPENAI_API_KEY"] = "1193fe53e44a4c2ba132cf5a5259f9e6"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://desai-pac-azure-open-ai-1.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "despacai-gpt4"

eval_llm  = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    temperature = 0.2
)

class Grade(BaseModel):
    score: float = Field(description="Get the graded score")
    explanation: str = Field(description="Get the explantion")

def get_qa_eval_chain( question, answer):

  parser = JsonOutputParser(pydantic_object=Grade)

  fstring_1 = """You are an expert professor specialized in grading students' answers to questions. Provide the grading score and very very short explanation.

  {format_instructions}

  You are grading the following question:
  {question}

  You are grading the following students' answer:
  {answer}
  Grade, how accurate is this answer on a scale of 1-10?:
  Grade:

  Explantion:
  """

  prompt_template = PromptTemplate(
      input_variables=["question", "answer"],
      template=fstring_1,
      partial_variables={"format_instructions": parser.get_format_instructions()}
  )

  chain = prompt_template | eval_llm | parser


  return chain.invoke({"question": question, "answer":answer})


question = '"What Are the Different Types of Machine Learning?'
answer = 'Supervised Learning, Unsupervised Learnin'
# get_qa_eval_chain(eval_llm, question, answer)



from typing import List

class Question_generation(BaseModel):
    questions: List[str] = Field(description="Get the list of questions")

def get_resume(path):
  from langchain_community.document_loaders import PyPDFLoader
  from langchain_community.document_loaders import Docx2txtLoader

  if path.split('.')[-1] == 'pdf':
    loader = PyPDFLoader(path)
  elif path.split('.')[-1] == 'docx':
    loader = Docx2txtLoader(path)
  else:
    f_type = path.split('.')[-1]
    return f"File type {f_type} is not supported, supported types are 'pdf' and 'docx'."
  resume = loader.load()
  return resume[0].page_content


def get_db_chain( jd, resume_path):
  qb_parser = JsonOutputParser(pydantic_object=Question_generation)

  qb_fstring = """You are an expert interviewer specialized in asking techinal questions based on given resume and job description.
  Just ask the five questions.
  Always ensure that the technical questions are concise and based on skills, techniques, or tools that are common to both the resume and the job description.


  {format_instructions}

  Job description:
  {jd}

  Resume:
  {resume}


  Questions:
  1.
  """

  qb_prompt_template = PromptTemplate(
      input_variables=["jd", "resume"],
      template=qb_fstring,
      partial_variables={"format_instructions": qb_parser.get_format_instructions()}
  )

  qb_chain = qb_prompt_template | eval_llm | qb_parser


  return qb_chain.invoke({"jd": jd,"resume":get_resume(resume_path)})


jd = """
Role: Artificial Intelligence Engineer
Responsibilities:
- Design and implement machine learning models to solve complex problems using Python and relevant frameworks.

- Develop and maintain web applications using Django, ensuring seamless backend integration and high performance.

- Utilize NLP techniques and large language models to enhance the intelligence and functionality of applications.

- Collaborate with cross-functional teams to define clear specifications, features, and timelines.

- Conduct data collection, preprocessing, and analysis to optimize model accuracy and performance.

- Write clean, manageable code and maintain proper documentation for scalability and future code iterations.

- Stay updated with the latest advancements in AI, machine learning algorithms, and industry best practices.

- Participate in code reviews, unit testing, and debugging to ensure robust and error-free applications.

- Assist in the integration of AI technologies into existing systems, improving efficiency and effectiveness.

Required Skills & Qualifications:

- Bachelor’s or Master’s degree in Computer Science, Artificial Intelligence, or a related field.

- Proficient in Python, with solid experience in Django web framework.

- Strong foundation in machine learning, NLP, and familiarity with large language models like GPT or BERT.

- Experience with machine learning libraries and frameworks (e.g., TensorFlow, PyTorch, Scikit-Learn).

- Knowledge of RESTful API development and integration.

- Excellent problem-solving skills and ability to perform complex data analysis.

- Proven ability to manage and execute projects from conception to final product, within designated timelines.

- Strong communication and collaboration skills.

Preferred Skills:

- Experience with cloud platforms (AWS, GCP, Azure) and understanding of scalable infrastructure.

- Prior work with Docker, Kubernetes, and CI/CD pipelines.

- Publication record in AI/ML fields or contributions to open-source projects
"""

resume_path = '/content/Kumar_Deepankar.docx'
# get_db_chain(eval_llm, jd, resume_path)