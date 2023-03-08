package MovingAverageCrossStrategy;
use Moose;

has [qw(short_ma_period long_ma_period)] => (
    is       => 'ro',
    isa      => 'Int',
    required => 1
);

sub generate_signals {
    my ($self, $data) = @_;

    my $short_ma = $data->{'Close'}->rolling($self->short_ma_period)->mean();
    my $long_ma  = $data->{'Close'}->rolling($self->long_ma_period)->mean();

    $data->{'Signal'} = 0;
    $data->where($short_ma > $long_ma, {'Signal' => 1});
    $data->where($short_ma < $long_ma, {'Signal' => -1});
    $data->where($short_ma == $long_ma, {'Signal' => 0});

    return $data;
}

no Moose;
__PACKAGE__->meta->make_immutable;

1;