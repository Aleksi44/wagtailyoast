import { AnalysisWebWorker } from 'yoastseo';

// Run Yoast Worker

const worker = new AnalysisWebWorker(self);
worker.register();
