#from bard import bardHandler
from gpt3 import chatgptHandler
from dotenv import load_dotenv

import os

load_dotenv()


config = {
    "model":"gpt-3.5-turbo-0125",
    "token": os.environ.get("API_KEY"),
    "outputLanguage": "pt-br",
}
text = """
        Automatic Text Summarization (ATS) is the automatic process of transforming an original text
document into a shorter piece of text, using techniques of Natural Language Processing (NLP),
that highlights the most important information within it, according to a given criterion.
There is no doubt that one of the main uses of ATS systems is that they directly address the information overload problem (Edmunds and Morris, 2000). They allow a possible
reader to understand the content of the document without having to read it entirely. Other
ATS applications are keyphrase extraction (Hasan and Ng, 2014), document categorization
(Brandow et al., 1995), information retrieval (Tombros and Sanderson, 1998) and question answering (Morris et al., 1992).
The seminal work in ATS systems field is due to Luhn (1958) that used an approach that
mixes information about the frequency of words with some heuristics to summarize the text of
scientific papers. There are several different approaches to designing ATS systems today. In
this paper, we intend to present a comprehensive literature review on this topic. This is not an
easy task (Bullers et al., 2018). First, there are thousands of papers, and we have to face the
obvious question that is “Which set of the works should we include in this review?”. Second,
the papers use very different approaches. Thus, the second important question is “How do
we present these papers in a comprehensive way?”. We address the first question by adopting
a citation-based approach. That means we start with a few popular1 and well-known papers
about each topic we want to cover and we track the “backward citations” (papers that are
cited by the set of papers we knew beforehand) and the “forward citations” (newer papers
that cite the set of papers we knew beforehand). One clear challenge of this approach is to
avoid the popularity bias so common in recommendation systems (Park and Tuzhilin, 2008;
Hervas-Drane, 2008; Fleder and Hosanagar, 2009). We deal with this challenge by trying to
consider papers that cover different dimensions of the approach we are reviewing. In order to
answer the second question, we have tried to present the diverse approaches to ATS guided by
the mechanisms they use to generate a summary.
Our paper naturally relates to other reviews about this theme. We may classify these
reviews in terms of classical such as Edmundson and Wyllys (1961) and Paice (1990), topicspecific such as Rahman and Borah (2015) (query-based summarization), Pouriyeh et al. (2018)
(ontology-based summarization), Jalil et al. (2021) (extractive multi-document summarization)
and Alomari et al. (2022) (deep learning approaches to summarization), and general reviews like
ours such as Mridha et al. (2021) and El-Kassas et al. (2021). Although these latter works are
very related to ours in terms of general content, the presentation of our work is very different.
The models and mechanisms used to build such summaries drive our presentation. Thus, our
focus on models and mechanisms used in automatic text summarization aims to provide practical guidance for researchers or practitioners who are developing such systems. By emphasizing
these aspects of summarization, our review has the potential to offer unique insights that are not
covered by other works in the field, and may help to bridge the gap between the technique used
to build the model and the practical application in summarization. Furthermore, besides presenting the models used to generate the summaries, we also present the most popular datasets,
a compendium of evaluation techniques, and an exploration of the public python libraries that
one can use to implement the task of ATS2
.
We organize the manuscript as follows: Section 2 presents a taxonomy used to classify ATS
systems. Section 3 summarizes the content of other surveys about ATS systems. Section 4
describes the datasets used to explore ATS systems. Section 5 illustrates the basic topology
of an ATS system. In Section 6, we present the approaches to extractive summarization
"""


try:
    gpt_handler =  chatgptHandler(config, text)
    gpt_handler.sendMessage()
    print(gpt_handler.summary)


    #bard_handler = bardHandler()

except Exception as e:
    print(e)


