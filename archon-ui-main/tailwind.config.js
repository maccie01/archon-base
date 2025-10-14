export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  // Tailwind v4 uses @theme in CSS for most configuration
  // This config is minimal and only for content scanning
  safelist: [
    // Force generation of data-active styles for tabs
    'data-active:bg-blue-pastel/30',
    'data-active:text-blue-pastel-dark',
    'data-active:bg-purple-pastel/30',
    'data-active:text-purple-pastel-dark',
    'data-active:bg-pink-pastel/30',
    'data-active:text-pink-pastel-dark',
    'data-active:bg-orange-pastel/30',
    'data-active:text-orange-pastel-dark',
    'data-active:bg-teal-pastel/30',
    'data-active:text-teal-pastel-dark',
    'data-active:bg-green-pastel/30',
    'data-active:text-green-pastel-dark',
    'data-active:border',
    'data-active:border-blue-pastel/50',
    'data-active:border-purple-pastel/50',
    'data-active:border-pink-pastel/50',
    'data-active:border-orange-pastel/50',
    'data-active:border-teal-pastel/50',
    'data-active:border-green-pastel/50',
    'data-active:shadow-sm',
  ],
}