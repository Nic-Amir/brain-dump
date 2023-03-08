#!bin/usr/bin/perl

use strict;
use warnings;
use 5.18.0;
use lib 'Test';
use Person;
use OptionPrice;

my $x1 = Person->new( name => "nic", age=> 24, gender=> "male");
 
my $bsm = OptionPrice->new(strike => 100,
    spot => 105,
    t => 1,
    discount_rate => 0.05,
    mu => 0.03,
    vol => 0.2,
    payouttime_code => "continuous",
    payout_type => "call",
    contract_type => "european",);

my $price = $bsm->calculate_price;

say $price;

