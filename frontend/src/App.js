import React, { useState } from 'react';
import {
  Container,
  TextField,
  Button,
  Paper,
  Typography,
  Box,
  CircularProgress,
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8082';

function App() {
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [studyPlan, setStudyPlan] = useState(null);
  const [error, setError] = useState(null);

  const createNewSession = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/new-session`);
      console.log('Session creation response:', response.data);
      setSessionId(response.data.id);
      setError(null);
      return response.data;
    } catch (err) {
      setError('Failed to create session. Please try again.');
      console.error('Session creation error:', err);
      throw err;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const sessionResponse = await createNewSession();
      const currentSessionId = sessionResponse.id;
      
      console.log('Session ID:', currentSessionId);
      console.log('Input:', input);
      
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        text: input,
        session_id: currentSessionId,
        user_id: "student_9yo"
      });
      
      setStudyPlan(response.data.study_plan);
      setInput('');
    } catch (err) {
      setError('Failed to generate study plan. Please try again.');
      console.error('Chat error:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderStudyPlan = () => {
    if (!studyPlan) return null;

    return (
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Your Study Plan
        </Typography>
        
        <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            Overview
          </Typography>
          
          {studyPlan.original_plan.study_plan.map((day, index) => (
            <Box key={index} sx={{ mb: 2 }}>
              <Typography variant="h6">
                Day {day.day}: {day.topic}
              </Typography>
              <Typography variant="body1">
                Duration: {day.duration}
              </Typography>
            </Box>
          ))}

          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Additional Notes
            </Typography>
            <Typography variant="body1">
              {studyPlan.original_plan.additional_notes}
            </Typography>
          </Box>
        </Paper>

        <Typography variant="h5" gutterBottom>
          Detailed Lesson Plans
        </Typography>
        
        {studyPlan.detailed_topics.map((topic, index) => (
          <Paper key={index} elevation={2} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Day {topic.day_plan.day}: {topic.topic}
            </Typography>
            
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Introduction
              </Typography>
              <Typography variant="body1" paragraph>
                {topic.day_plan.detailed_content.introduction.explanation}
              </Typography>
              
              <Typography variant="subtitle1" gutterBottom>
                Main Content
              </Typography>
              <Typography variant="body1" paragraph>
                {topic.day_plan.detailed_content.main_content.explanation}
              </Typography>
              
              <Typography variant="subtitle1" gutterBottom>
                Practice Section
              </Typography>
              <Typography variant="body1" paragraph>
                {topic.day_plan.detailed_content.practice_section.practice_problems.join(', ')}
              </Typography>
              
              <Typography variant="subtitle1" gutterBottom>
                Summary
              </Typography>
              <Typography variant="body1">
                {topic.day_plan.detailed_content.summary.key_takeaways.join(', ')}
              </Typography>
            </Box>
          </Paper>
        ))}
      </Box>
    );
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Learning Assistant
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            fullWidth
            label="What would you like to learn?"
            variant="outlined"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            disabled={loading || !input.trim()}
          >
            {loading ? <CircularProgress size={24} /> : 'Generate Study Plan'}
          </Button>
        </Box>

        {error && (
          <Typography color="error" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}

        {renderStudyPlan()}
      </Paper>
    </Container>
  );
}

export default App; 