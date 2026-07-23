"use client";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export function Hero() {
  return (
    <section className="w-full py-24 bg-gradient-to-br from-sky-50 to-white text-center">
      <div className="max-w-5xl mx-auto px-6">
        <h1 className="text-5xl font-extrabold leading-tight mb-6">
          Generate Animated Educational Videos with AI ✨
        </h1>
        <p className="text-xl text-gray-600 mb-10">
          Just type a topic and get a Manim-rendered video with AI narration. Perfect for teachers, students, and creators.
        </p>
        <Link href="/generate">
          <Button size="lg" className="text-lg px-8 py-6 rounded-2xl shadow-xl">
            Try It Now
          </Button>
        </Link>
      </div>
    </section>
  );
}
