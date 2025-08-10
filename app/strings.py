grammar_word_prompt = """
### ANALYSIS TASK
Analyze the following Korean video transcript and extract language learning content organized by proficiency level ({proficiency_level}):

{transcript}

### EXTRACTION GUIDELINES

1. **GRAMMAR POINTS**
   - Extract grammar structures actually used in the transcript
   - Focus on the most practical and commonly used patterns
   - Match each grammar point to its exact timestamp in the video
   - Categorize by function (e.g., expressing ability, making requests)

2. **VOCABULARY**
   - Extract key words and phrases from the transcript
   - Prioritize commonly used expressions (marked as "important")
   - Include natural collocations and useful phrases
   - Ensure accurate timestamps for each entry

3. **DIFFICULTY CALIBRATION**
   - Beginner: Focus on basic sentence structures, particles, and essential vocabulary
   - Intermediate: Include conditional forms, connecting endings, and idiomatic expressions
   - Advanced: Capture nuanced grammar, formal/informal variations, and specialized vocabulary

### RESPONSE FORMAT
Return a JSON object with the following structure:

{
    "grammar": [
        {
            "id": "1",
            "title": "~습니다/~ㅂ니다",
            "description": "Formal present tense ending used to state facts or describe current situations",
            "example": "저는 학생입니다", 
            "translation": "I am a student",
            "difficulty": "beginner",
            "function": "stating facts",
            "timestamp": "1:20"
        }
    ],
    "vocabulary": [
        {
            "id": "1",
            "word": "도와주세요",
            "meaning": "Please help me",
            "context": "When asking for assistance",
            "type": "important",
            "timestamp": "0:05"
        }
    ]
}

### GRAMMAR REFERENCE
Below is a reference of Korean grammar patterns. Only include patterns that actually appear in the transcript:

#### PARTICLES
- 은/는 – Topic markers (contrast, introduction)
- 이/가 – Subject markers (emphasis, identification)
- 을/를 – Object markers
- 에/에서 – Location markers (at, in)
- 에게/한테 – Direction markers (to someone)
- 와/과/하고/랑 – Conjunctive particles (and, with)
- 의 – Possessive particle ('s, of)
- 도 – Inclusion particle (also, too)
- (으)로 – Direction/method particle (to, by means of)

#### VERB ENDINGS
- Present tense: -아/어요, -ㅂ니다/습니다
- Past tense: -았/었어요, -았/었습니다
- Future tense: -(으)ㄹ 거예요, -겠어요
- Negative forms: -지 않아요, 안-, 못-
- Progressive: -고 있어요
- Desire: -고 싶어요
- Request: -(으)세요, -(으)십시오
- Ability: -(으)ㄹ 수 있어요/없어요
- Obligation: -아/어야 해요
- Permission: -아/어도 돼요
- Prohibition: -하면 안 돼요
- Intention: -(으)려고 해요, -(으)ㄹ게요

#### CONNECTORS
- Sequence: -고, -아/어서
- Reason: -아/어서, -(으)니까, -기 때문에
- Contrast: -지만, -는데
- Condition: -(으)면, -(으)려면
- Purpose: -(으)러, -(으)려고, -기 위해서
- Time: -(으)ㄹ 때, -기 전에, -(으)ㄴ 후에
- Simultaneous action: -(으)면서

Extract as many relevant grammar points and vocabulary items as possible, but only include those actually present in the transcript. Ensure all timestamps are accurate.

### ADDITIONAL GRAMMAR REFERENCE BY PROFICIENCY LEVEL

#### A1 LEVEL
- Expressing acts of service: Verb Stem + -아/어 주다 (문을 열어 주세요)
- Sequential actions: Verb Stem + -고 나서 + Next Action (밥을 먹고 나서 공부했어요)
- Measure words for specific items: Object + Number + Measure Word (자동차 한 대를 샀어요)
- Measure words for living beings: Object + Number + Measure Word (사람 세 명이 왔어요)
- Measure words for general objects: Object + Number + Measure Word (사과 세 개 샀어)
- Irregular adjectives: ㅂ Irregular: 쉽다 → 쉬워요 (이 책은 정말 쉬워)
- Past progressive tense: Verb Stem + 고 있었다 (어제 이 시간에 저는 책을 읽고 있었어요)
- Present progressive tense: Verb stem + -고 있다 (나는 지금 밥을 먹고 있다)
- Common prepositions: 안, 밖, 앞, 위, 아래, 왼쪽, 오른쪽 + article (내 동생은 학교안에 있다)
- Basic sentence structure: Subject + Verb (나는 걸어요)
- Negative Form: 안 + Verb/Adjective (저는 브로콜리를 안 먹어요)
- Present Tense: Verb + 아요 (닫아요)
- Past Tense: Verb + 았어요 (닫았어요)
- Future Tense: Verb + -ㄹ거예요 (갈 거예요)
- Asking questions: 누구, 언제, 어디 etc (선생님이 누구에요?)
- Direction particle: Noun + (으)로 (왼쪽으로 직진하세요)
- Place & time particles: Noun + 에/에서 (나는 학교에 가요)
- Possessive Particle: Noun + 의 (미나의 가방)
- Topic/Subject particles: Noun + 은/는/이/가 (이것은 만화책이에요)
- Expressing Too/Also: Subject + Object + 도 (나는 한국도 방문하고 싶다)
- Because in Korean: Verb/adjective ending with 아 + 서 (내가 가서 파티가 끝났어)
- But in Korean: Phrase 1 + 하지만 + Phrase 2 (나는 졸리다. 하지만 나는 숙제를 끝내야 한다)
- Expressing desire: Verb + ~하기를 원하다 (그녀는 주말에 수영 하기를 원한다)
- Korean plurals: Noun + 들 (아이들)
- Using adjectives: Subject (은/는/이/가) + Infinitive Adjective (수진이는 예쁘다)
- Expressing capacity: Verb + ᄅ/을 수 있다 (나는 영어를 유창하게 구사할 수 있다)
- Or in Korean: Noun + (이)나 + Noun (중식이나 한식을 먹고 싶어요)

#### A2 LEVEL
- Before and after: Verb Stem + 기 전에/후에 + Main Action (수업을 듣기 전에 책을 읽어요)
- Cause and effect: Verb/Adjective Stem + -아/어서 + Result (밥을 많이 먹어서 배가 불러요)
- Trying actions: Subject + Verb Stem + 아/어 보다 (한번 읽어 보세요)
- Expressing probability: S + V + -ㄹ/을 것 같다 (비가 올 것 같아요)
- Compound verbs: Verb Stem + Verb Stem + 다 (새로운 레스토랑을 찾아보고 싶어요)
- Additional particles: Noun + 까지/밖에/마저 (저는 내일 아침 7시까지 회사에 가야 해요)
- Future progressive: Verb Stem + 고 있을 것이다 (내일 이 시간에 저는 책을 읽고 있을 거예요)
- Expressing potential: Verb + ᄅ/을 수도 있다 (내일 비가 올 수도 있다)
- Irregular verbs: ㄷ changes to ㄹ before vowel (듣다 → 들어요)
- Include & exclude: A + 은/는 + B + 을/를 + 포함한다 (선물은 몇 권의 책을 포함한다)
- Expressing 'only': Subject + 만 (+이) (학부모만이 학교에 들어갈 수 있다)
- Expressing "seem/look like": Subject + adjective + ᄂ 듯 + verb (그녀는 행복한 듯 하다)
- As much as: Noun + 만큼/정도 (형만큼 먹을 수 있니?)
- Expressing shall we: Verb + ᄅ/을까요 (서점에 갈까요?)
- Expressing suggestion: Verb + ᄇ/읍시다 (내일 서울에 갑시다)
- Expressing in order to: Verb + 려고/러 (좋은 대학에 가려고 공부를 열심히 한다)
- Expressing might be: Verb + ᄅ것 같다 (내일비가올것같다)
- With and together: Subject + 랑/이랑 + object + verb (점심은 누구랑 먹었어?)
- Relative quantities: 정말, 진짜, 너무 etc (진짜 니 친구가 그렇게 말했어?)
- Expressing intention: Subject + Object + 를/을 하려고 하다 (나는 오늘부터 운동을 하려고 한다)
- Making requests: Verb + 주 + 다 (봐주다)
- Expressing if/if not: 면 + Phrase (공부를 열심히 하면, 좋은 대학에 갈 수 있어)
- Expressing and: Noun + 랑/이랑 (나는 친구랑 숙제를 할 꺼에요)
- Formal words: Noun + 님/분 (선생님)
- Asking & giving directions: 어느 + 쪽으로/방향으로/길로 + 가면될까요? (동명초등학교로 가려면 어느쪽으로 가면 될까요?)
- Creating adverbs: Adjective + 게/하게 (조용하게)
- Imperative form: Verb + -세요/으세요 (조용히 말하세요)

#### B1 LEVEL
- Expressing certainty/doubt: S + V + -에 틀림없다 (그가 범인인 게 틀림없어요)
- Conditional sentences: Verb/Adjective Stem + (으)면 (기차가 늦으면 연락해 주세요)
- Assumptions & Predictions: Verb/Adjective Stem + -겠 (수업이 곧 끝나겠지?)
- Using 중: Noun + 중 (지금 수업 중이니 나중에 전화해 주세요)
- Honorific verbs: Verb + 시다 (오다 → 오시다)
- As soon as: A + ~자마자 + B (그는 일이 끝나자마자 딸을픽업하러 갔다)
- Expressing instead: Noun + 대신 (오늘은 동생 대신 내가 식사값을지불하겠다)
- Expressing almost: Verb + ᄅ/을 뻔하다 (나는 수업시간에 잠들 뻔 했어)
- Quoted sentences: S + O + V in past tense + ᄊ다고 (말)했어요 (그는 숙제를 끝냈다고 했어요)
- Simultaneous actions: Verb + (으)면서 (누나는 점심을 먹으면서 신문을 읽는다)
- Whenever and when: Verb + ᄅ 때 (청소를할때음악을틀어놓는다)
- Expressing certainty: Verb + 다고 (그녀가 내일 파티에 온다고 생각한다)
- Adjectives to nouns: Verb + 음 (적다 → 적음)
- Verbs to nouns: Verb without '다' + 는것/기 (공부하기)
- Superlatives: A + (이)가/(은)는 + B + 보다 더 + adjective (노란 공이 파란공보다 더 커요)
- Expressing must: Verb + ~야(만) 한다 (공부를 해야(만) 한다)
- Using honorifics: Name + 씨 (수진씨)

#### B2 LEVEL
- Using 도록: Verb + -도록 (고양이를 기를 수 있도록 할 거예요)
- Passive voice: Verb + -이/-히/-리/-기 (놓다 → 놓이다)
- Even though: Subject + Verb + ㄴ지만 (그는 아프지만 수업에참여합니다)
- Expressing emphasis: Verb + ㄹ 뿐이다 (그의 행동은 그녀를 더 밀어낼뿐이다)
- Expressing surprise: Subject + Verb + (는) 구나/네/군 (그녀가 부산에서 오는구나)
- Expressing similarity: Subject + noun + 처럼 + verb (그녀는 그녀의 엄마처럼보인다)
- Expressing hope: Verb + 기를 바라다 (그는 좋은 대학에 가기를 바란다)

"""
### ... (rest of the code remains the same)

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
