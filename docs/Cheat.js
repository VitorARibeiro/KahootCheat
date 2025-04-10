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
        if (questionText) { // Ignora perguntas sem texto
            const choices = question.choices || [];
            const answers = choices.map(option => ({
                answer: option.answer,
                correct: option.correct || false // Marca se a resposta é correta
            }));
            finalDictionary[questionText] = answers;
        }
    });
    return finalDictionary;
}