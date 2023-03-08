#!/usr/bin/perl

use strict;
use warnings;

sub black_scholes {
    my ($s, $k, $r, $d, $t, $sigma, $option_type) = @_;

    my $d1 = (log($s / $k) + ($r - $d + 0.5 * $sigma ** 2) * $t) / ($sigma * sqrt($t));
    my $d2 = $d1 - $sigma * sqrt($t);

    my $call_price = $s * exp(-$d * $t) * cdf_standard_normal($d1) - $k * exp(-$r * $t) * cdf_standard_normal($d2);
    my $put_price = $k * exp(-$r * $t) * cdf_standard_normal(-$d2) - $s * exp(-$d * $t) * cdf_standard_normal(-$d1);

    return $option_type eq 'call' ? $call_price : $put_price;
}

my @a = (0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429);
my @b = (0.2316419, 0.3989423, 0.0, -0.3989423, 0.0);

sub cdf_standard_normal {
    my ($x) = @_;
    my $t = 1 / (1 + 0.2316419 * abs($x));
    my $d = 0.3989423 * exp(-$x * $x / 2);
    my $p = 1 - $d * (($a[0] * $t + $a[1] * $t ** 2 + $a[2] * $t ** 3 + $a[3] * $t ** 4 + $a[4] * $t ** 5) / ($b[0] * $t + $b[1] * $t ** 2 + $b[2] * $t ** 3 + $b[3] * $t ** 4 + $b[4] * $t ** 5));
    return $x < 0 ? 1 - $p : $p;
}


sub main {
    print "Enter stock price: ";
    my $s = <STDIN>;
    chomp $s;

    print "Enter strike price: ";
    my $k = <STDIN>;
    chomp $k;

    print "Enter risk-free rate: ";
    my $r = <STDIN>;
    chomp $r;

    print "Enter dividend yield: ";
    my $d = <STDIN>;
    chomp $d;

    print "Enter time to expiration (in years): ";
    my $t = <STDIN>;
    chomp $t;

    print "Enter volatility: ";
    my $sigma = <STDIN>;
    chomp $sigma;

    print "Enter option type (call or put): ";
    my $option_type = <STDIN>;
    chomp $option_type;

    my $price = black_scholes($s, $k, $r, $d, $t, $sigma, $option_type);
    print "Option price: $price\n";
}

main();

