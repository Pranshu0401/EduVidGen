import { Hero } from "../components/ui/hero";
import { Features } from "../components/ui/feature";
import { Footer } from "../components/ui/footer";
import Navbar from "../components/ui/Navbar";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white text-gray-900">
      <Navbar />
      <main>
        <Hero />
        <Features />
      </main>
      <Footer />
    </div>
  );
}
