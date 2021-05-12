
export default class ResultContainers {
  /**
   * Controller of Yoast results
   *
   * @param {Result} results Results of yoastseo module
   */
  constructor(results) {
    this.results = results;
    this.readabilityContainer = $('#yoast_results_readability');
    this.seoContainer = $('#yoast_results_seo');

  }

  /**
   * Clear Results
   *
   * @param {object} $container Jquery selector of the container
   * @returns {void}
   */
  static clear($container) {
    const $success = $container.find('.success');
    const $errors = $container.find('.errors');
    $success.empty();
    $errors.empty();
  }

  /**
   * Get HTML icon if success or error according to the score
   *
   * @param {AssessmentResult} result Assessment result of yoastseo module
   * @return {string}
   */
  static scoreIcon(result) {
    return ResultContainers.isSuccessResult(result)
      ? '<i class="icon icon-tick"></i>'
      : '<i class="icon icon-cross"></i>';
  }


  /**
   * Check if AssessmentResult is scored successfully
   *
   * @param {AssessmentResult} result Assessment result of yoastseo module
   * @return {boolean}
   */
  static isSuccessResult(result) {
    return result.score >= 9;
  }

  /**
   * Get Jquery instance of success or errors container
   *
   * @param {object} $container Jquery selector of the container
   * @param {AssessmentResult} result Assessment result of yoastseo module
   * @return {object}
   */
  static getStatusContainer($container, result) {
    const $success = $container.find('.success');
    const $errors = $container.find('.errors');
    return ResultContainers.isSuccessResult(result) ? $success : $errors;
  }

  /**
   * Remove unwanted rules of yoastseo module
   *
   * @param {AssessmentResult} result Assessment result of yoastseo module
   * @return {object}
   */
  static filterUnwantedResult(result) {
    // FIXME: singleH1 does not work, fix it with Yoast
    const unwanted = [
      'singleH1',
    ];
    // eslint-disable-next-line no-underscore-dangle
    return unwanted.indexOf(result._identifier) === -1;
  }

  /**
   * Add AssessmentResult object to the container
   *
   * @param {object} $container Jquery selector of the container
   * @param {AssessmentResult} result Assessment result of yoastseo module
   * @return {void}
   */
  static addResult($container, result) {
    if (result.score !== 0 && ResultContainers.filterUnwantedResult(result)) {
      ResultContainers.getStatusContainer($container, result).append(
        `<li>${ResultContainers.scoreIcon(result)} ${result.text}</li>`,
      );
    }
  }

  /**
   * Synchronize the UI with results of yoastseo module
   *
   * @return {void}
   */
  sync() {
    // Clean containers
    ResultContainers.clear(this.readabilityContainer);
    ResultContainers.clear(this.seoContainer);

    // Append Data
    Array.prototype.forEach.call(this.results.result.readability.results, (el) => {
      ResultContainers.addResult(this.readabilityContainer, el);
    });
    Array.prototype.forEach.call(this.results.result.seo[''].results, (el) => {
      ResultContainers.addResult(this.seoContainer, el);
    });
  }
}
