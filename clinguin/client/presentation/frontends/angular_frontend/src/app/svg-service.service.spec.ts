import { TestBed } from '@angular/core/testing';

import { SvgServiceService } from './svg-service.service';

describe('SvgServiceService', () => {
  let service: SvgServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SvgServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
