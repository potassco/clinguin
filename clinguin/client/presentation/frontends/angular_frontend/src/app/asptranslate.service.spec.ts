import { TestBed } from '@angular/core/testing';

import { ASPtranslateService } from './asptranslate.service';

describe('ASPtranslateService', () => {
  let service: ASPtranslateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ASPtranslateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
