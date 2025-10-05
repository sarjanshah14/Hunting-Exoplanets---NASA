import { motion } from 'framer-motion';
import { Card } from '../components/ui/Card';
import { BookOpen, Telescope, Cpu, Rocket, ExternalLink } from 'lucide-react';

const resources = [
  {
    icon: Telescope,
    title: 'How NASA Finds Exoplanets',
    description: 'Exoplanets are detected primarily through the transit method, where a planet passes in front of its host star, causing a slight dimming in the star\'s brightness. By analyzing these periodic dips in light, scientists can determine the planet\'s size, orbital period, and distance from its star.',
    color: 'cyan',
    links: [
      { text: 'NASA Exoplanet Exploration', url: 'https://exoplanets.nasa.gov/' },
      { text: 'Transit Method Explained', url: 'https://exoplanets.nasa.gov/alien-worlds/ways-to-find-a-planet/' }
    ]
  },
  {
    icon: Rocket,
    title: 'Kepler Mission (2009-2013)',
    description: 'The Kepler Space Telescope was NASA\'s first planet-hunting mission, monitoring 150,000 stars simultaneously in a single patch of sky. It discovered over 2,600 confirmed exoplanets and revolutionized our understanding of planetary systems. Kepler showed that planets are common in our galaxy.',
    color: 'blue',
    links: [
      { text: 'Kepler Mission Overview', url: 'https://www.nasa.gov/mission_pages/kepler/overview/index.html' }
    ]
  },
  {
    icon: Rocket,
    title: 'K2 Mission (2014-2018)',
    description: 'After Kepler\'s reaction wheels failed, the mission was reinvented as K2. Instead of staring at one field, K2 observed different fields along the ecliptic plane for 80 days each. This extended mission discovered over 500 additional exoplanets and studied a diverse range of cosmic phenomena.',
    color: 'violet',
    links: [
      { text: 'K2 Mission Details', url: 'https://www.nasa.gov/mission/k2' }
    ]
  },
  {
    icon: Rocket,
    title: 'TESS Mission (2018-Present)',
    description: 'The Transiting Exoplanet Survey Satellite is surveying nearly the entire sky, focusing on finding planets around nearby bright stars. TESS is discovering planets that are ideal for follow-up characterization with the James Webb Space Telescope, enabling detailed atmospheric studies.',
    color: 'green',
    links: [
      { text: 'TESS Mission Home', url: 'https://www.nasa.gov/tess-transiting-exoplanet-survey-satellite' }
    ]
  },
  {
    icon: Cpu,
    title: 'Machine Learning in Exoplanet Detection',
    description: 'ML algorithms process vast amounts of light curve data to identify patterns consistent with planetary transits. These models are trained on known exoplanets and false positives, learning to distinguish genuine signals from stellar activity, instrumental noise, and other artifacts. Modern approaches achieve 90%+ accuracy.',
    color: 'orange',
    links: [
      { text: 'NASA ML Research', url: 'https://www.nasa.gov/feature/ames/artificial-intelligence-nasa-data-used-to-discover-eighth-planet-circling-distant-star' }
    ]
  },
  {
    icon: BookOpen,
    title: 'Understanding Light Curves',
    description: 'A light curve is a graph showing how a star\'s brightness changes over time. When a planet transits, the light curve shows a characteristic dip. The depth tells us the planet\'s size relative to the star, the duration reveals the orbital geometry, and the shape provides clues about the planet\'s atmosphere.',
    color: 'pink',
    links: [
      { text: 'Light Curve Tutorial', url: 'https://exoplanets.nasa.gov/resources/2236/what-is-a-light-curve/' }
    ]
  }
];

const colorClasses = {
  cyan: 'from-cyan-500 to-blue-600',
  blue: 'from-blue-500 to-indigo-600',
  violet: 'from-violet-500 to-purple-600',
  green: 'from-green-500 to-emerald-600',
  orange: 'from-orange-500 to-red-600',
  pink: 'from-pink-500 to-rose-600'
};

export function Learning() {
  return (
    <div className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 bg-clip-text text-transparent mb-4">
            Learning Center
          </h1>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Explore the science behind exoplanet detection and NASA's groundbreaking missions
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {resources.map((resource, idx) => {
            const Icon = resource.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
              >
                <Card className="p-8 h-full" hover>
                  <div className="flex items-start space-x-4 mb-4">
                    <div className={`p-4 rounded-xl bg-gradient-to-br ${colorClasses[resource.color as keyof typeof colorClasses]} shadow-lg`}>
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                    <h2 className="text-2xl font-bold text-white flex-1">{resource.title}</h2>
                  </div>

                  <p className="text-gray-300 leading-relaxed mb-6">{resource.description}</p>

                  <div className="space-y-2">
                    <p className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
                      Learn More
                    </p>
                    {resource.links.map((link, linkIdx) => (
                      <a
                        key={linkIdx}
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-2 text-cyan-400 hover:text-cyan-300 transition-colors group"
                      >
                        <ExternalLink className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        <span>{link.text}</span>
                      </a>
                    ))}
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-12"
        >
          <Card className="p-8 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border-cyan-500/30">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-white mb-4">Want to Contribute?</h2>
              <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
                AstroKit is an open research platform. Whether you're a student, educator, or professional astronomer,
                you can contribute to exoplanet research by using these tools to analyze data and share your findings
                with the scientific community.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <a
                  href="https://github.com/nasa"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 bg-cyan-500 hover:bg-cyan-600 text-white font-semibold rounded-lg transition-colors inline-flex items-center space-x-2"
                >
                  <span>Visit NASA on GitHub</span>
                  <ExternalLink className="w-4 h-4" />
                </a>
                <a
                  href="https://exoplanetarchive.ipac.caltech.edu/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors inline-flex items-center space-x-2"
                >
                  <span>NASA Exoplanet Archive</span>
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
