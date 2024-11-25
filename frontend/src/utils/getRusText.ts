export function translateToRus(area: string): string {
    const translations: { [key: string]: string } = {
        'anterior torso': 'Передняя часть торса',
        'lower extremity': 'Нижняя конечность',
        'head/neck': 'Голова/шея',
        'upper extremity': 'Верхняя конечность',
        'posterior torso': 'Задняя часть торса',
        'palms/soles': 'Ладони/подошвы',
        'oral/genital': 'Полость рта/гениталии',
        'lateral torso': 'Боковая часть торса',
    };

    return translations[area] || 'Перевод не найден';
}
export function translateToLat(area: string): string {
    const translations: { [key: string]: string } = {
        'Передняя часть торса': 'anterior torso',
        'Нижняя конечность': 'lower extremity',
        'Голова/шея': 'head/neck',
        'Верхняя конечность': 'upper extremity',
        'Задняя часть торса': 'posterior torso',
        'Ладони/подошвы': 'palms/soles',
        'Полость рта/гениталии': 'oral/genital',
        'Боковая часть торса': 'lateral torso',
    };
    return translations[area] || 'Перевод не найден';
}
