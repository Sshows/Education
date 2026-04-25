export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function postForecast(payload: unknown) {
  try {
    const res = await fetch(`${API_URL}/api/forecast`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('forecast_failed');
    return await res.json();
  } catch {
    if (process.env.NODE_ENV === 'development') {
      return {
        grant_probability: 34,
        paid_status: 'eligible',
        grant_status: 'eligible_for_competition',
        confidence: 'medium',
        error_margin_pp: 12,
        explanation: {
          threshold_check: 'mock fallback',
          confidence_reasons: ['backend_unavailable_dev_fallback'],
          conflicts: ['Есть расхождение в источниках'],
        },
        sources: [],
      };
    }
    throw new Error('Backend unavailable');
  }
}
