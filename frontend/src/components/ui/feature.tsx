export function Features() {
  const features = [
    {
      title: "AI-Powered Narration",
      description: "Uses LLM to generate educational explanations and voiceovers.",
    },
    {
      title: "Manim-Based Animation",
      description: "Renders videos using Python’s Manim library in 3D or 2D.",
    },
    {
      title: "Personal Dashboard",
      description: "Each user gets a dashboard to store and rewatch generated videos.",
    },
    {
      title: "Custom Topics",
      description: "Just type a topic and get an accurate, visual explanation video.",
    },
  ];

  return (
    <section className="py-20 bg-white">
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-center mb-10">
          Powerful Features for Modern Learning
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="p-6 bg-gray-50 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition"
            >
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
