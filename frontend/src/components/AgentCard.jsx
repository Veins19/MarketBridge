import React from "react";
import { Card, CardContent, Typography } from "@mui/material";
// eslint-disable-next-line no-unused-vars
import { motion } from "framer-motion";

export default function AgentCard({ title, content }) {
  return (
    <motion.div whileHover={{ scale: 1.05 }}>
      <Card sx={{ p: 2 }}>
        <CardContent>
          <Typography variant="h6">{title}</Typography>
          <Typography>{content}</Typography>
        </CardContent>
      </Card>
    </motion.div>
  );
}
