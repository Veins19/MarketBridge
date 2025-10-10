import React, { useState } from "react";
import { runCampaign } from "../api";
import AgentCard from "../components/AgentCard";
import { Container, TextField, Button, Typography, Grid } from "@mui/material";

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [product, setProduct] = useState("");
  const [results, setResults] = useState(null);

  const handleRun = async () => {
    const res = await runCampaign(query, product);
    setResults(res);
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h3" align="center" gutterBottom>
        🤖 AIMarketer
      </Typography>
      <Typography variant="h6" align="center" gutterBottom>
        Autonomous Multi-Agent Campaign Planner
      </Typography>

      <Grid container spacing={2} justifyContent="center" sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <TextField fullWidth label="Enter campaign request" value={query} onChange={(e) => setQuery(e.target.value)} />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField fullWidth label="Enter product name" value={product} onChange={(e) => setProduct(e.target.value)} />
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" size="large" onClick={handleRun}>
            🚀 Run Campaign Planner
          </Button>
        </Grid>
      </Grid>

      {results && (
        <Grid container spacing={4}>
          {Object.keys(results).map((key) => (
            <Grid item xs={12} md={4} key={key}>
              <AgentCard title={key} content={results[key]} />
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
}
