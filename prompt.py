grammar_word_prompt = """
I will provide you with a transcript.
Select grammar and words from the given transcript.
Based on the given transcript, select grammar and words that can aid in language learning.

Example transcript :
    [{'duration': 5.16, 'start': 9.559, 'text': '서울대학교 치대 다녀왔습니다 치 진짜'},
     {'duration': 6.68, 'start': 16.72, 'text': '치대대 하나 둘'}]

Example of return JSON :
{
    "grammar": [{
        id: "1",
        title: "~습니다",
        description:
        "Express ability to do something. Express ability to do something",
        type: "writing",
        timestamp: "1:20",
    },
    {
        id: "2",
        title: "~(이)ㄹ/를 수 없다",
        description: "Express inability to do something",
        type: "writing",
        timestamp: "1:30",
    }]
    "vocabulary": [
    {
        id: "1",
        word: "도와주세요",
        meaning: "Please help me",
        type: "important",
        timestamp: "0:05",
    },
   
}

Timestamp is the time when the grammar or vocabulary appears in the transcript.
Because the transcript is sorted by time, it is easy to find the location of the grammar or vocabulary.
Be careful with timestamp and make sure the timestamp is correct!
Be carefutl with a grammar and word! It must to be from the given transcript!
Do not take a to simple word like 저는, 나는, 이름이, etc.
Return as many grammar and words as possible.
"""

summary_prompt = """
I will provide you with a list of grammar and words.
Summarize the given grammar and words so i can learn them easily. Or recall every word and grammar that i have learned.

Example of return JSON :
[
  {
    id: "1",
    title: "Key Grammar Points",
    content: [
      "Basic sentence structure: Subject + Object + Verb",
      "Formal vs. Informal speech levels",
      "Past, Present, and Future tense markers",
    ],
  },
]

"""

question_prompt = """
I will provide you with a list of grammar and words.
Make a multiple choice test with the given grammar and words.

Example of return JSON :
[
  {
    id: "1",
    question: "Which is the correct formal way to say 'hello'?",
    options: ["안녕", "안녕하세요", "안녕히 가세요", "안녕히 계세요"],
    correctAnswer: 1,
  },
  {
    id: "2",
    question: "What is the meaning of '감사합니다'?",
    options: ["Hello", "Goodbye", "Thank you", "I'm sorry"],
    correctAnswer: 2,
  },
  {
    id: "3",
    question: "Which particle is used to mark the subject of a sentence?",
    options: ["을/를", "이/가", "은/는", "에서"],
    correctAnswer: 1,
  },
  {
    id: "4",
    question: "What is the correct way to say 'I like something' in Korean?",
    options: [
      "저는 ~을/를 좋아합니다",
      "~을/를 좋아합니다",
      "저는 ~을/를 좋아요",
      "~을/를 좋아요",
    ],
    correctAnswer: 0,
  },
  {
    id: "5",
    question: "What is the meaning of the Korean word '도서관'?",
    options: ["Library", "School", "University", "Bookstore"],
    correctAnswer: 0,
  },
  {
    id: "6",
    question: "What is the correct way to say 'What is your name?' in Korean?",
    options: [
      "당신의 이름은 무엇입니까?",
      "당신의 이름은?",
      "당신의 이름을 알려주세요",
      "당신의 이름을",
    ],
    correctAnswer: 0,
  },
];


"""