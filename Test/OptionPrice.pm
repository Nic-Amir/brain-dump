package OptionPrice;
use Moose;

has [qw(strike spot t discount_rate mu vol)]=> (is => 'ro', isa => 'Num', required => 1);
has [qw(payouttime_code payout_type contract_type )] => (is => 'ro', isa => 'Str', required => 1);

sub calculate_price {
    my ($self) = @_;

    my $d1 = (log($self->spot/$self->strike) + ($self->discount_rate + 0.5 * $self->vol ** 2) * $self->t) / ($self->vol * sqrt($self->t));
    my $d2 = $d1 - $self->vol * sqrt($self->t);
    
    my $price;
    if ($self->payout_type eq "call") {
        $price = $self->spot * norm_cdf($d1) - $self->strike * exp(-$self->discount_rate * $self->t) * norm_cdf($d2);
    } elsif ($self->payout_type eq "put") {
        $price = $self->strike * exp(-$self->discount_rate * $self->t) * norm_cdf(-$d2) - $self->spot * norm_cdf(-$d1);
    }
    
    if ($self->payouttime_code eq "continuous") {
        $price *= exp(-$self->mu * $self->t);
    } elsif ($self->payouttime_code eq "discrete") {
        $price *= (1 + $self->mu * $self->t) ** (-1);
    }
    
    return $price;
}

sub norm_cdf {
    my ($x) = @_;
    my $k = 1 / (1 + 0.2316419 * abs($x));
    my $p = (0.31938153 * $k - 0.356563782 * $k ** 2 + 1.781477937 * $k ** 3 - 1.821255978 * $k ** 4 + 1.330274429 * $k ** 5) * exp(-0.5 * $x ** 2) / sqrt(2 * 3.14159265358979);
    return $x >= 0 ? 1 - $p : $p;
}

__PACKAGE__->meta->make_immutable;

1;