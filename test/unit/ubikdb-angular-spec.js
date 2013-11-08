//
// test/unit/ubikdb-angular-spec.js
//
describe("Unit: ubikDB for Angular", function() {

    var ubikDBProvider;
    beforeEach(module('ubikDB', function(ubikDBProvider) {
        ubikDBProvider = ubikDBProvider;
    }));

    it('loads the provider', inject(function(ubikDB) {
        var db = new ubikDB.prototype.constructor();
    }));

    it('has bind method defined', inject(function(ubikDB) {
        var db = new ubikDB.prototype.constructor();
        expect(db.bind).to.be.a('function');
    }));

});
