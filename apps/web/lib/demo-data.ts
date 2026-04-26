export const programs = [
  {
    code: 'B057',
    name: 'Информационные технологии',
    subjects: 'Математика + информатика',
    cutoff: 82,
    demand: 'Высокий конкурс',
  },
  {
    code: 'B058',
    name: 'Информационная безопасность',
    subjects: 'Математика + информатика',
    cutoff: 88,
    demand: 'Очень высокий конкурс',
  },
  {
    code: 'B059',
    name: 'Коммуникации и коммуникационные технологии',
    subjects: 'Математика + информатика',
    cutoff: 76,
    demand: 'Стабильный конкурс',
  },
  {
    code: 'B157',
    name: 'Робототехника и мехатроника',
    subjects: 'Математика + физика',
    cutoff: 84,
    demand: 'Растущий спрос',
  },
];

export const universities = [
  { id: 'iitu', name: 'МУИТ / IITU', city: 'Алматы', focus: 'IT, безопасность, data', cutoff: 84 },
  { id: 'aitu', name: 'Astana IT University', city: 'Астана', focus: 'Software, AI, product', cutoff: 86 },
  { id: 'sdu', name: 'SDU University', city: 'Каскелен', focus: 'Инженерия и бизнес', cutoff: 82 },
  { id: 'kbtu', name: 'KBTU', city: 'Алматы', focus: 'Технологии, финансы, нефть', cutoff: 91 },
  { id: 'satbayev', name: 'Satbayev University', city: 'Алматы', focus: 'Инженерия и промышленность', cutoff: 74 },
  { id: 'kaznu', name: 'КазНУ имени аль-Фараби', city: 'Алматы', focus: 'Наука, IT, естественные науки', cutoff: 78 },
];

export const sources = [
  { title: 'НЦТ', url: 'https://testcenter.kz', status: 'официальный источник' },
  { title: 'МНВО РК', url: 'https://www.gov.kz', status: 'нормативные публикации' },
  { title: 'Приёмные комиссии вузов', url: '#', status: 'проверять по вузу' },
];

export const deadlines = [
  { title: 'Подача заявлений на грант', period: 'после публикации правил конкурса', source: 'МНВО / НЦТ' },
  { title: 'Творческие экзамены', period: 'по графику выбранного вуза', source: 'приёмная комиссия' },
  { title: 'Зачисление', period: 'после официальных итогов конкурса', source: 'вуз' },
];
