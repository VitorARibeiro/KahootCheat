export async function requestQuestion(gameId) {
    const apiUrl = `https://corsproxy.io/https://play.kahoot.it/rest/kahoots/${gameId}`;
    const response = await fetch(apiUrl);
    const data = await response.json();
    return data.questions;
}

export function parser(input) {
    const finalDictionary = {};
    input.forEach(question => {
        const questionText = question.question;
        if (questionText) {
            const choices = question.choices || [];
            const correctAnswers = choices
                .filter(option => option.correct === true)
                .map(option => option.answer);
            finalDictionary[questionText] = correctAnswers;
        }
    });
    return finalDictionary;
}