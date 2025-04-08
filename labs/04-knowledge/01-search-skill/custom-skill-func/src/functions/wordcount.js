const { app } = require('@azure/functions');

// Array of stop words to be ignored
const stopwords = [
  '',
  'i',
  'me',
  'my',
  'myself',
  'we',
  'our',
  'ours',
  'ourselves',
  'you',
  'youre',
  'youve',
  'youll',
  'youd',
  'your',
  'yours',
  'yourself',
  'yourselves',
  'he',
  'him',
  'his',
  'himself',
  'she',
  'shes',
  'her',
  'hers',
  'herself',
  'it',
  'its',
  'itself',
  'they',
  'them',
  'their',
  'theirs',
  'themselves',
  'what',
  'which',
  'who',
  'whom',
  'this',
  'that',
  'thatll',
  'these',
  'those',
  'am',
  'is',
  'are',
  'was',
  'were',
  'be',
  'been',
  'being',
  'have',
  'has',
  'had',
  'having',
  'do',
  'does',
  'did',
  'doing',
  'a',
  'an',
  'the',
  'and',
  'but',
  'if',
  'or',
  'because',
  'as',
  'until',
  'while',
  'of',
  'at',
  'by',
  'for',
  'with',
  'about',
  'against',
  'between',
  'into',
  'through',
  'during',
  'before',
  'after',
  'above',
  'below',
  'to',
  'from',
  'up',
  'down',
  'in',
  'out',
  'on',
  'off',
  'over',
  'under',
  'again',
  'further',
  'then',
  'once',
  'here',
  'there',
  'when',
  'where',
  'why',
  'how',
  'all',
  'any',
  'both',
  'each',
  'few',
  'more',
  'most',
  'other',
  'some',
  'such',
  'no',
  'nor',
  'not',
  'only',
  'own',
  'same',
  'so',
  'than',
  'too',
  'very',
  'can',
  'will',
  'just',
  'dont',
  'should',
  'shouldve',
  'now',
  'arent',
  'couldnt',
  'didnt',
  'doesnt',
  'hadnt',
  'hasnt',
  'havent',
  'isnt',
  'mightnt',
  'mustnt',
  'neednt',
  'shant',
  'shouldnt',
  'wasnt',
  'werent',
  'wont',
  'wouldnt',
];

app.http('wordcount', {
  methods: ['POST'],
  authLevel: 'anonymous',
  handler: async (request, context) => {
    context.log('JavaScript HTTP trigger function processed a request.');

    const body = await request.json();

    if (body && body.values) {
      const vals = body.values;
      const res = { values: [] };

      for (const rec in vals) {
        // Get the record ID and text for this input
        const resVal = { recordId: vals[rec].recordId, data: {} };
        let txt = vals[rec].data.text;

        // remove punctuation and numerals
        txt = txt.replace(/[^ A-Za-z_]/g, '').toLowerCase();

        // Get an array of words
        const words = txt.split(' ');

        // count instances of non-stopwords
        const wordCounts = {};
        for (let i = 0; i < words.length; ++i) {
          const word = words[i];
          if (!stopwords.includes(word)) {
            wordCounts[word] = (wordCounts[word] || 0) + 1;
          }
        } // Get unique words (not counting duplicates)
        const uniqueWords = Object.keys(wordCounts);

        // Add the filtered words to the response
        resVal.data.text = uniqueWords;

        res.values[rec] = resVal;
      }

      return {
        jsonBody: res,
        headers: {
          'Content-Type': 'application/json',
        },
      };
    } else {
      return {
        status: 400,
        jsonBody: { errors: [{ message: 'Invalid input' }] },
        headers: {
          'Content-Type': 'application/json',
        },
      };
    }
  },
});
