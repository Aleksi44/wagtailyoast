

export default class ResultContainers {
  constructor(results) {
    this.results = results;
    this.readabilityContainer = $('#yoast_results_readability');
    this.seoContainer = $('#yoast_results_seo');
  }

  static clear($container) {
    const $success = $container.find('.success');
    const $errors = $container.find('.errors');
    $success.empty();
    $errors.empty();
  }

  static scoreIcon(result) {
    return ResultContainers.isSuccessResult(result)
      ? '<i class="icon icon-tick"></i>'
      : '<i class="icon icon-cross"></i>';
  }

  static isSuccessResult(result) {
    return result.score >= 9;
  }

  static addResult($container, result) {
    const $success = $container.find('.success');
    const $errors = $container.find('.errors');
    const $dest = ResultContainers.isSuccessResult(result) ? $success : $errors;
    if (result.score !== 0) {
      $dest.append(
        `<li>${ResultContainers.scoreIcon(result)} ${result.text}</li>`,
      );
    }
  }

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
