export default class WithContext {
  constructor(context) {
    this.context = context;
    this.baseUrl = `${window.location.protocol}//${window.location.host}`;
    this.isDev = process.env.NODE_ENV === 'development';
  }
}
