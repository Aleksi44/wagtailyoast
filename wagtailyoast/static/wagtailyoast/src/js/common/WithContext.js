export default class WithContext {
  /**
   * Abstraction to get context from python.
   *
   * @param {object} context The context of wagtailyoast/context.py
   */
  constructor(context) {
    this.context = context;
    this.baseUrl = `${window.location.protocol}//${window.location.host}`;
    this.isDev = process.env.NODE_ENV === 'development';
  }
}
