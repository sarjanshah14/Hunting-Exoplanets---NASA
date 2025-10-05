import { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  gradient?: boolean;
}

export function Card({ children, className = '', hover = false, gradient = false }: CardProps) {
  const baseClasses = gradient
    ? 'bg-gradient-to-br from-gray-800/40 via-gray-900/40 to-gray-800/40 backdrop-blur-sm border border-cyan-500/20 rounded-xl shadow-xl'
    : 'bg-gray-800/40 backdrop-blur-sm border border-gray-700/50 rounded-xl shadow-xl';

  return (
    <motion.div
      className={`${baseClasses} ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { scale: 1.02, borderColor: 'rgba(6, 182, 212, 0.5)' } : {}}
    >
      {children}
    </motion.div>
  );
}
