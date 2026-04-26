import type { NextConfig } from 'next';
import path from 'node:path';

const nextConfig: NextConfig = {
  outputFileTracingRoot: path.join(process.cwd(), '../..'),
  // Allow Next.js to transpile the shared package
  transpilePackages: ['@ent-grant/shared'],
};

export default nextConfig;
