import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  eslint: {
    // TODO: Remove this once ESLint errors are fixed
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
