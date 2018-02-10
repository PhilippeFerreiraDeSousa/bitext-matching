function upperFirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

const flags = {
  'english': 'gb',
  'french': 'fr',
  'russian': 'ru',
  'german': 'de',
  'portuguese': 'pt',
  'spanish': 'es',
  'italian': 'it',
  'romanian': 'ro'
}

const languageOptions = Object.keys(flags).map((language, idx) => ({key: idx, value: language, flag: flags[language], text: upperFirst(language)}))

export { flags, languageOptions }
