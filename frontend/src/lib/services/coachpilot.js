/**
 * CoachPilot API Service
 * Provides methods to interact with the CoachPilot API for generating structured coaching content
 */

// API base URL - adjust based on your environment
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

/**
 * Available content formats for structured coaching content
 */
export const ContentFormats = {
  CHECKLIST: 'checklist',
  KANBAN: 'kanban',
  TIMELINE: 'timeline',
  MINDMAP: 'mindmap',
  ACTION_PLAN: 'action_plan',
  DAILY_ROUTINE: 'daily_routine',
  COMPARISON_TABLE: 'comparison_table',
  SMART_GOALS: 'smart_goals'
};

/**
 * Generate structured coaching content based on a query
 * @param {object} options - The request options
 * @param {string} options.query - The coaching query or topic to address
 * @param {Array<string>} options.formats - The desired content formats (from ContentFormats)
 * @param {number} options.topK - Number of book chunks to retrieve (default: 5)
 * @param {boolean} options.includeSources - Whether to include book sources (default: true)
 * @param {boolean} options.detailedResponse - Whether to include detailed explanations (default: false)
 * @returns {Promise<object>} The generated coaching content
 */
export async function generateCoachContent({
  query,
  formats = [ContentFormats.ACTION_PLAN],
  topK = 5,
  includeSources = true,
  detailedResponse = false,
}) {
  try {
    const response = await fetch(`${API_BASE_URL}/coachpilot/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        formats,
        top_k: topK,
        include_sources: includeSources,
        detailed_response: detailedResponse,
        // Let the backend determine the correct database path
        // Don't specify db_path to allow the backend to use its default
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to generate coaching content');
    }

    return response.json();
  } catch (error) {
    console.error('Error generating coaching content:', error);
    throw error;
  }
}

/**
 * Test the CoachPilot API connection
 * @returns {Promise<object>} The API status
 */
export async function testCoachPilotApi() {
  try {
    const response = await fetch(`${API_BASE_URL}/coachpilot/test`);
    
    if (!response.ok) {
      throw new Error('CoachPilot API is not available');
    }

    return response.json();
  } catch (error) {
    console.error('Error testing CoachPilot API:', error);
    throw error;
  }
}