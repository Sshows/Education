// ============================================================
// ENT SUBJECTS — Single Source of Truth
// Shared between apps/web and apps/api (via this package)
// ============================================================

// --------------- Subject IDs ---------------

export type SubjectId =
  | 'history_kazakhstan'
  | 'math_literacy'
  | 'reading_literacy'
  // profile subjects
  | 'mathematics'
  | 'physics'
  | 'informatics'
  | 'chemistry'
  | 'biology'
  | 'geography'
  | 'world_history'
  | 'foreign_language'
  | 'fundamentals_of_law'
  | 'kazakh_language'
  | 'russian_language'
  | 'kazakh_literature'
  | 'russian_literature'
  | 'creative_exam';

export interface SubjectMeta {
  id: SubjectId;
  label: { ru: string; kk: string; en: string };
  isMandatory: boolean;
  isProfile: boolean;
}

export const MANDATORY_SUBJECTS: SubjectMeta[] = [
  {
    id: 'history_kazakhstan',
    label: { ru: 'История Казахстана', kk: 'Қазақстан тарихы', en: 'History of Kazakhstan' },
    isMandatory: true,
    isProfile: false,
  },
  {
    id: 'math_literacy',
    label: { ru: 'Математическая грамотность', kk: 'Математикалық сауаттылық', en: 'Mathematical Literacy' },
    isMandatory: true,
    isProfile: false,
  },
  {
    id: 'reading_literacy',
    label: { ru: 'Грамотность чтения', kk: 'Оқу сауаттылығы', en: 'Reading Literacy' },
    isMandatory: true,
    isProfile: false,
  },
];

export const PROFILE_SUBJECTS: SubjectMeta[] = [
  {
    id: 'mathematics',
    label: { ru: 'Математика', kk: 'Математика', en: 'Mathematics' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'physics',
    label: { ru: 'Физика', kk: 'Физика', en: 'Physics' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'informatics',
    label: { ru: 'Информатика', kk: 'Информатика', en: 'Informatics' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'chemistry',
    label: { ru: 'Химия', kk: 'Химия', en: 'Chemistry' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'biology',
    label: { ru: 'Биология', kk: 'Биология', en: 'Biology' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'geography',
    label: { ru: 'География', kk: 'География', en: 'Geography' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'world_history',
    label: { ru: 'Всемирная история', kk: 'Дүниежүзі тарихы', en: 'World History' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'foreign_language',
    label: { ru: 'Иностранный язык', kk: 'Шет тілі', en: 'Foreign Language' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'fundamentals_of_law',
    label: { ru: 'Основы права', kk: 'Құқық негіздері', en: 'Fundamentals of Law' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'kazakh_language',
    label: { ru: 'Казахский язык', kk: 'Қазақ тілі', en: 'Kazakh Language' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'russian_language',
    label: { ru: 'Русский язык', kk: 'Орыс тілі', en: 'Russian Language' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'kazakh_literature',
    label: { ru: 'Казахская литература', kk: 'Қазақ әдебиеті', en: 'Kazakh Literature' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'russian_literature',
    label: { ru: 'Русская литература', kk: 'Орыс әдебиеті', en: 'Russian Literature' },
    isMandatory: false,
    isProfile: true,
  },
  {
    id: 'creative_exam',
    label: { ru: 'Творческий экзамен', kk: 'Шығармашылық емтихан', en: 'Creative Exam' },
    isMandatory: false,
    isProfile: true,
  },
];

export const ALL_SUBJECTS: SubjectMeta[] = [...MANDATORY_SUBJECTS, ...PROFILE_SUBJECTS];

// --------------- Subject Combinations ---------------

export type DataQuality = 'official' | 'imported' | 'secondary' | 'demo' | 'unknown';

export interface SubjectCombination {
  /** Canonical sorted key: always smaller id first */
  key: string;
  subject1: SubjectId;
  subject2: SubjectId;
  label: { ru: string; kk: string; en: string };
  aliases: string[];
  category: { ru: string; en: string };
  examples: string[];
  /** Program group codes that require this combination (demo mapping) */
  programGroupCodes: string[];
  dataQuality: DataQuality;
}

/** Build a canonical key: sorted alphabetically */
export function subjectPairKey(a: SubjectId | string, b: SubjectId | string): string {
  return [a, b].sort().join('+');
}

export const SUBJECT_COMBINATIONS: SubjectCombination[] = [
  {
    key: subjectPairKey('mathematics', 'physics'),
    subject1: 'mathematics',
    subject2: 'physics',
    label: { ru: 'Математика + Физика', kk: 'Математика + Физика', en: 'Mathematics + Physics' },
    aliases: ['физмат', 'матфиз', 'физ-мат', 'мат-физ'],
    category: { ru: 'Инженерия / технические науки', en: 'Engineering / Technical' },
    examples: ['Инженерия', 'Строительство', 'Энергетика', 'Транспорт', 'Горное дело', 'Педагогика физики/математики'],
    programGroupCodes: ['B071', 'B062', 'B063', 'B064', 'B065', 'B074', 'B157'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('informatics', 'mathematics'),
    subject1: 'mathematics',
    subject2: 'informatics',
    label: { ru: 'Математика + Информатика', kk: 'Математика + Информатика', en: 'Mathematics + Informatics' },
    aliases: ['инфомат', 'матинф', 'инф-мат', 'мат-инф'],
    category: { ru: 'IT / цифровые технологии', en: 'IT / Digital Technologies' },
    examples: [
      'B057 Информационные технологии',
      'B058 Информационная безопасность',
      'B059 Коммуникации и коммуникационные технологии',
      'B157 Информационные системы и технологии',
      'Computer Science',
      'Software Engineering',
      'Cybersecurity',
      'Data Science',
    ],
    programGroupCodes: ['B057', 'B058', 'B059', 'B157'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('geography', 'mathematics'),
    subject1: 'mathematics',
    subject2: 'geography',
    label: { ru: 'Математика + География', kk: 'Математика + География', en: 'Mathematics + Geography' },
    aliases: ['матгео', 'геомат'],
    category: { ru: 'Экономика / менеджмент / логистика', en: 'Economics / Management / Logistics' },
    examples: ['Экономика', 'Менеджмент', 'Финансы', 'Учёт и аудит', 'Туризм', 'Логистика'],
    programGroupCodes: ['B044', 'B045', 'B046', 'B047'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('biology', 'chemistry'),
    subject1: 'biology',
    subject2: 'chemistry',
    label: { ru: 'Биология + Химия', kk: 'Биология + Химия', en: 'Biology + Chemistry' },
    aliases: ['химбио', 'биохим', 'хим-био', 'био-хим'],
    category: { ru: 'Медицина / биология / агрономия', en: 'Medicine / Biology / Agriculture' },
    examples: ['Медицина', 'Стоматология', 'Фармация', 'Биология', 'Педагогика биологии/химии', 'Сельское хозяйство', 'Ветеринария'],
    programGroupCodes: ['B084', 'B085', 'B086', 'B087', 'B088'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('biology', 'geography'),
    subject1: 'biology',
    subject2: 'geography',
    label: { ru: 'Биология + География', kk: 'Биология + География', en: 'Biology + Geography' },
    aliases: ['биогео', 'геобио'],
    category: { ru: 'Педагогика / экология / география', en: 'Pedagogy / Ecology / Geography' },
    examples: ['Педагогика', 'Экология', 'География', 'Природопользование'],
    programGroupCodes: ['B001', 'B002', 'B003'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('foreign_language', 'world_history'),
    subject1: 'foreign_language',
    subject2: 'world_history',
    label: { ru: 'Иностранный язык + Всемирная история', kk: 'Шет тілі + Дүниежүзі тарихы', en: 'Foreign Language + World History' },
    aliases: ['англвсемирка', 'ин язык всемирная история', 'иняз всемирка'],
    category: { ru: 'Языки / международные отношения', en: 'Languages / International Relations' },
    examples: ['Иностранная филология', 'Переводческое дело', 'Международные отношения', 'Педагогика иностранного языка'],
    programGroupCodes: ['B036', 'B018'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('foreign_language', 'geography'),
    subject1: 'geography',
    subject2: 'foreign_language',
    label: { ru: 'География + Иностранный язык', kk: 'География + Шет тілі', en: 'Geography + Foreign Language' },
    aliases: ['геоангл', 'геоиняз'],
    category: { ru: 'Туризм / международные программы', en: 'Tourism / International' },
    examples: ['Туризм', 'Регионоведение', 'Международные программы'],
    programGroupCodes: [],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('fundamentals_of_law', 'world_history'),
    subject1: 'world_history',
    subject2: 'fundamentals_of_law',
    label: { ru: 'Всемирная история + Основы права', kk: 'Дүниежүзі тарихы + Құқық негіздері', en: 'World History + Fundamentals of Law' },
    aliases: ['истправо', 'всемирка право', 'всемирная история право'],
    category: { ru: 'Право / юриспруденция', en: 'Law / Jurisprudence' },
    examples: ['Право', 'Юриспруденция', 'Правоохранительная деятельность'],
    programGroupCodes: ['B049'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('geography', 'world_history'),
    subject1: 'world_history',
    subject2: 'geography',
    label: { ru: 'Всемирная история + География', kk: 'Дүниежүзі тарихы + География', en: 'World History + Geography' },
    aliases: ['истгео', 'всемирка география'],
    category: { ru: 'Гуманитарные / социальные науки', en: 'Humanities / Social Sciences' },
    examples: ['История', 'Археология', 'Регионоведение', 'Социальные науки'],
    programGroupCodes: [],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('kazakh_language', 'kazakh_literature'),
    subject1: 'kazakh_language',
    subject2: 'kazakh_literature',
    label: { ru: 'Казахский язык + Казахская литература', kk: 'Қазақ тілі + Қазақ әдебиеті', en: 'Kazakh Language + Kazakh Literature' },
    aliases: ['казлит', 'қазлит', 'казахский язык литература'],
    category: { ru: 'Филология / языки', en: 'Philology / Languages' },
    examples: ['Филология', 'Педагогика языка и литературы'],
    programGroupCodes: ['B037'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('russian_language', 'russian_literature'),
    subject1: 'russian_language',
    subject2: 'russian_literature',
    label: { ru: 'Русский язык + Русская литература', kk: 'Орыс тілі + Орыс әдебиеті', en: 'Russian Language + Russian Literature' },
    aliases: ['руслит', 'русский язык литература'],
    category: { ru: 'Филология / языки', en: 'Philology / Languages' },
    examples: ['Филология', 'Педагогика языка и литературы'],
    programGroupCodes: ['B037'],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('chemistry', 'physics'),
    subject1: 'chemistry',
    subject2: 'physics',
    label: { ru: 'Химия + Физика', kk: 'Химия + Физика', en: 'Chemistry + Physics' },
    aliases: ['химфиз', 'физхим'],
    category: { ru: 'Химическая инженерия / материалы', en: 'Chemical Engineering / Materials' },
    examples: ['Химическая инженерия', 'Материаловедение', 'Технологические направления'],
    programGroupCodes: [],
    dataQuality: 'demo',
  },
  {
    key: subjectPairKey('creative_exam', 'creative_exam'),
    subject1: 'creative_exam',
    subject2: 'creative_exam',
    label: { ru: 'Творческий экзамен', kk: 'Шығармашылық емтихан', en: 'Creative Exam' },
    aliases: ['творческий', 'творч', 'creative'],
    category: { ru: 'Искусство / спорт / дизайн', en: 'Arts / Sport / Design' },
    examples: ['Дизайн', 'Искусство', 'Спорт', 'Творческие направления'],
    programGroupCodes: [],
    dataQuality: 'demo',
  },
];

// --------------- Alias map ---------------

const ALIAS_MAP = new Map<string, string>(); // alias -> key
const KEY_MAP = new Map<string, SubjectCombination>(); // key -> combo

for (const combo of SUBJECT_COMBINATIONS) {
  KEY_MAP.set(combo.key, combo);
  for (const alias of combo.aliases) {
    ALIAS_MAP.set(alias.toLowerCase().replace(/\s+/g, ' ').trim(), combo.key);
  }
}

// --------------- Helper Functions ---------------

/** Normalise a raw string to a known SubjectId, or return null. */
export function normalizeSubjectId(input: string): SubjectId | null {
  const normalized = input.toLowerCase().trim().replace(/[-\s]+/g, '_');
  const found = ALL_SUBJECTS.find(
    (s) =>
      s.id === normalized ||
      s.label.ru.toLowerCase() === input.toLowerCase().trim() ||
      s.label.kk.toLowerCase() === input.toLowerCase().trim() ||
      s.label.en.toLowerCase() === input.toLowerCase().trim(),
  );
  return found?.id ?? null;
}

/** Build a normalised, order-insensitive pair key for two subjects. */
export function normalizeSubjectPair(a: string, b: string): string {
  const idA = normalizeSubjectId(a) ?? a;
  const idB = normalizeSubjectId(b) ?? b;
  return subjectPairKey(idA, idB);
}

/** Look up a combination by canonical pair key (order-insensitive). */
export function getSubjectCombinationByPair(
  subject1: SubjectId | string,
  subject2: SubjectId | string,
): SubjectCombination | null {
  const key = subjectPairKey(subject1, subject2);
  return KEY_MAP.get(key) ?? null;
}

/** Look up a combination by alias (case-insensitive). */
export function getSubjectCombinationByAlias(alias: string): SubjectCombination | null {
  const key = ALIAS_MAP.get(alias.toLowerCase().trim());
  if (!key) return null;
  return KEY_MAP.get(key) ?? null;
}

/** Returns true if a program group code is matched by the given subject pair. */
export function programMatchesSubjectPair(
  programGroupCode: string,
  subject1: SubjectId | string,
  subject2: SubjectId | string,
): boolean {
  const combo = getSubjectCombinationByPair(subject1, subject2);
  if (!combo) return false;
  return combo.programGroupCodes.includes(programGroupCode);
}

/** Returns an error message if subjects are incompatible with a program group, or null if OK. */
export function validateProfileSubjectsForProgram(
  programGroupCode: string,
  subject1: SubjectId | string,
  subject2: SubjectId | string,
): string | null {
  if (programMatchesSubjectPair(programGroupCode, subject1, subject2)) {
    return null;
  }
  // Find what is required
  const requiredCombo = SUBJECT_COMBINATIONS.find((c) => c.programGroupCodes.includes(programGroupCode));
  if (!requiredCombo) {
    return `Программа ${programGroupCode} не найдена в базе сочетаний.`;
  }
  return (
    `Программа ${programGroupCode} требует: ${requiredCombo.label.ru}. ` +
    `Вы выбрали: ${subjectPairKey(subject1, subject2)}.`
  );
}

/** Returns all combinations that include the given program group code. */
export function getRecommendedProgramGroupsForSubjectPair(
  subject1: SubjectId | string,
  subject2: SubjectId | string,
): string[] {
  const combo = getSubjectCombinationByPair(subject1, subject2);
  return combo?.programGroupCodes ?? [];
}

// --------------- Demo Program Groups ---------------

export type ProgramGroupMeta = {
  code: string;
  name: { ru: string; en: string };
  subject1: SubjectId;
  subject2: SubjectId;
  subjectPairKey: string;
  subjectCombinationLabel: string;
  dataQuality: DataQuality;
  category: string;
};

export const DEMO_PROGRAM_GROUPS: ProgramGroupMeta[] = [
  // IT
  { code: 'B057', name: { ru: 'Информационные технологии', en: 'Information Technologies' }, subject1: 'mathematics', subject2: 'informatics', subjectPairKey: subjectPairKey('mathematics', 'informatics'), subjectCombinationLabel: 'Математика + Информатика', dataQuality: 'demo', category: 'IT' },
  { code: 'B058', name: { ru: 'Информационная безопасность', en: 'Information Security' }, subject1: 'mathematics', subject2: 'informatics', subjectPairKey: subjectPairKey('mathematics', 'informatics'), subjectCombinationLabel: 'Математика + Информатика', dataQuality: 'demo', category: 'IT' },
  { code: 'B059', name: { ru: 'Коммуникации и коммуникационные технологии', en: 'Communications and Communication Technologies' }, subject1: 'mathematics', subject2: 'informatics', subjectPairKey: subjectPairKey('mathematics', 'informatics'), subjectCombinationLabel: 'Математика + Информатика', dataQuality: 'demo', category: 'IT' },
  { code: 'B157', name: { ru: 'Информационные системы и технологии', en: 'Information Systems and Technologies' }, subject1: 'mathematics', subject2: 'informatics', subjectPairKey: subjectPairKey('mathematics', 'informatics'), subjectCombinationLabel: 'Математика + Информатика', dataQuality: 'demo', category: 'IT' },
  // Engineering
  { code: 'B071', name: { ru: 'Горное дело и добыча полезных ископаемых', en: 'Mining and Extraction' }, subject1: 'mathematics', subject2: 'physics', subjectPairKey: subjectPairKey('mathematics', 'physics'), subjectCombinationLabel: 'Математика + Физика', dataQuality: 'demo', category: 'Инженерия' },
  { code: 'B062', name: { ru: 'Электротехника и энергетика', en: 'Electrical Engineering and Energy' }, subject1: 'mathematics', subject2: 'physics', subjectPairKey: subjectPairKey('mathematics', 'physics'), subjectCombinationLabel: 'Математика + Физика', dataQuality: 'demo', category: 'Инженерия' },
  { code: 'B063', name: { ru: 'Электротехника и автоматизация', en: 'Electrical Engineering and Automation' }, subject1: 'mathematics', subject2: 'physics', subjectPairKey: subjectPairKey('mathematics', 'physics'), subjectCombinationLabel: 'Математика + Физика', dataQuality: 'demo', category: 'Инженерия' },
  { code: 'B064', name: { ru: 'Механика и металлообработка', en: 'Mechanics and Metalworking' }, subject1: 'mathematics', subject2: 'physics', subjectPairKey: subjectPairKey('mathematics', 'physics'), subjectCombinationLabel: 'Математика + Физика', dataQuality: 'demo', category: 'Инженерия' },
  { code: 'B065', name: { ru: 'Автотранспортные средства', en: 'Motor Vehicles' }, subject1: 'mathematics', subject2: 'physics', subjectPairKey: subjectPairKey('mathematics', 'physics'), subjectCombinationLabel: 'Математика + Физика', dataQuality: 'demo', category: 'Инженерия' },
  { code: 'B074', name: { ru: 'Градостроительство и гражданское строительство', en: 'Urban Planning and Civil Engineering' }, subject1: 'mathematics', subject2: 'physics', subjectPairKey: subjectPairKey('mathematics', 'physics'), subjectCombinationLabel: 'Математика + Физика', dataQuality: 'demo', category: 'Инженерия' },
  // Medicine
  { code: 'B084', name: { ru: 'Сестринское дело', en: 'Nursing' }, subject1: 'biology', subject2: 'chemistry', subjectPairKey: subjectPairKey('biology', 'chemistry'), subjectCombinationLabel: 'Биология + Химия', dataQuality: 'demo', category: 'Медицина' },
  { code: 'B085', name: { ru: 'Фармация', en: 'Pharmacy' }, subject1: 'biology', subject2: 'chemistry', subjectPairKey: subjectPairKey('biology', 'chemistry'), subjectCombinationLabel: 'Биология + Химия', dataQuality: 'demo', category: 'Медицина' },
  { code: 'B086', name: { ru: 'Общая медицина', en: 'General Medicine' }, subject1: 'biology', subject2: 'chemistry', subjectPairKey: subjectPairKey('biology', 'chemistry'), subjectCombinationLabel: 'Биология + Химия', dataQuality: 'demo', category: 'Медицина' },
  { code: 'B087', name: { ru: 'Стоматология', en: 'Dentistry' }, subject1: 'biology', subject2: 'chemistry', subjectPairKey: subjectPairKey('biology', 'chemistry'), subjectCombinationLabel: 'Биология + Химия', dataQuality: 'demo', category: 'Медицина' },
  { code: 'B088', name: { ru: 'Педиатрия', en: 'Pediatrics' }, subject1: 'biology', subject2: 'chemistry', subjectPairKey: subjectPairKey('biology', 'chemistry'), subjectCombinationLabel: 'Биология + Химия', dataQuality: 'demo', category: 'Медицина' },
  // Pedagogy
  { code: 'B001', name: { ru: 'Педагогика и психология', en: 'Pedagogy and Psychology' }, subject1: 'biology', subject2: 'geography', subjectPairKey: subjectPairKey('biology', 'geography'), subjectCombinationLabel: 'Биология + География', dataQuality: 'demo', category: 'Педагогика' },
  { code: 'B002', name: { ru: 'Дошкольное обучение и воспитание', en: 'Preschool Education' }, subject1: 'biology', subject2: 'geography', subjectPairKey: subjectPairKey('biology', 'geography'), subjectCombinationLabel: 'Биология + География', dataQuality: 'demo', category: 'Педагогика' },
  { code: 'B003', name: { ru: 'Педагогика и методика начального обучения', en: 'Primary Education Pedagogy' }, subject1: 'biology', subject2: 'geography', subjectPairKey: subjectPairKey('biology', 'geography'), subjectCombinationLabel: 'Биология + География', dataQuality: 'demo', category: 'Педагогика' },
  // Business
  { code: 'B044', name: { ru: 'Менеджмент и управление', en: 'Management' }, subject1: 'mathematics', subject2: 'geography', subjectPairKey: subjectPairKey('mathematics', 'geography'), subjectCombinationLabel: 'Математика + География', dataQuality: 'demo', category: 'Бизнес' },
  { code: 'B045', name: { ru: 'Аудит и налогообложение', en: 'Audit and Taxation' }, subject1: 'mathematics', subject2: 'geography', subjectPairKey: subjectPairKey('mathematics', 'geography'), subjectCombinationLabel: 'Математика + География', dataQuality: 'demo', category: 'Бизнес' },
  { code: 'B046', name: { ru: 'Финансы, экономика, банковское дело', en: 'Finance, Economics, Banking' }, subject1: 'mathematics', subject2: 'geography', subjectPairKey: subjectPairKey('mathematics', 'geography'), subjectCombinationLabel: 'Математика + География', dataQuality: 'demo', category: 'Бизнес' },
  { code: 'B047', name: { ru: 'Маркетинг и реклама', en: 'Marketing and Advertising' }, subject1: 'mathematics', subject2: 'geography', subjectPairKey: subjectPairKey('mathematics', 'geography'), subjectCombinationLabel: 'Математика + География', dataQuality: 'demo', category: 'Бизнес' },
  // Law
  { code: 'B049', name: { ru: 'Право', en: 'Law' }, subject1: 'world_history', subject2: 'fundamentals_of_law', subjectPairKey: subjectPairKey('world_history', 'fundamentals_of_law'), subjectCombinationLabel: 'Всемирная история + Основы права', dataQuality: 'demo', category: 'Право' },
  // Languages / Humanities
  { code: 'B036', name: { ru: 'Переводческое дело', en: 'Translation Studies' }, subject1: 'foreign_language', subject2: 'world_history', subjectPairKey: subjectPairKey('foreign_language', 'world_history'), subjectCombinationLabel: 'Иностранный язык + Всемирная история', dataQuality: 'demo', category: 'Языки' },
  { code: 'B037', name: { ru: 'Филология', en: 'Philology' }, subject1: 'kazakh_language', subject2: 'kazakh_literature', subjectPairKey: subjectPairKey('kazakh_language', 'kazakh_literature'), subjectCombinationLabel: 'Язык + Литература', dataQuality: 'demo', category: 'Языки' },
  { code: 'B018', name: { ru: 'Подготовка учителей иностранного языка', en: 'Foreign Language Teacher Education' }, subject1: 'foreign_language', subject2: 'world_history', subjectPairKey: subjectPairKey('foreign_language', 'world_history'), subjectCombinationLabel: 'Иностранный язык + Всемирная история', dataQuality: 'demo', category: 'Педагогика' },
];
