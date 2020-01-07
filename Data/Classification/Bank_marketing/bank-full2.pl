#!/usr/bin/perl

sub dequote(@);
sub getind($%);
sub getval($\@\%);
sub mkindex(@);
sub putval($$\@\%);
sub readlist($);
sub readln($);
sub writelist($@);
sub writeln($$);

# Define constants
$INFILE = "bank-full.csv";
$OUTFILE = "bank-full2.csv";
$BLANK = "";
$DLM = ";";
$ODLM = ",";
@YESNO = ("default", "loan", "y");

open STDIN, "<", $INFILE || die "Failure to open input file $INFILE: $!\n";
open STDOUT, ">", $OUTFILE || die "Failure to open output file $OUTFILE: $!\n";

@names = &dequote(&readlist(STDIN));
%index = &mkindex(@names);
&writelist(STDOUT, @names);

while (!eof(STDIN)) {
  @buf = &readlist(STDIN);
  foreach my $field (@YESNO) {
    my ($value0) = &dequote(&getval($field, \@buf, \%index));
    my $value;
    if ($value0 eq "yes") {$value = 1}
    elsif ($value0 eq "no") {$value = 0}
    &putval($field, $value, \@buf, \%index);
  }
  &writelist(STDOUT, @buf);
}

sub dequote(@) {
  my @retval = ();
  foreach my $value (@_) {
    $value =~ s/\"//g;
    push @retval, $value;
  }
  return @retval;
}

sub getind($%) {
  my ($name, %index) = @_;
  my $index = $index{$name};
  if (!defined($index)) {die "Field name $name not found\n"}
  return $index;
}

sub getval($\@\%) {
  my ($name, $pbuf, $pindex) = @_;
  my $index = &getind($name, %$pindex);
  return $$pbuf[$index];
}

sub mkindex(@) {
  my $nf = @name = @_;
  my %index;
  for (my $i = 0; $i < $nf; $i++) {$index{$name[$i]} = $i}
  return %index;
}

sub putval($$\@\%) {
  my ($name, $value, $pbuf, $pindex) = @_;
  my $index = &getind($name, %$pindex);
  $$pbuf[$index] = $value;
}

sub readlist($) {
  my ($fh) = @_;
  my $line = &readln($fh);
  return split($DLM, $line);
}

sub readln($) {
  my ($fh) = @_;
  my $line = <$fh>;
  chomp $line;
  return $line;
}

sub writelist($@) {
  my ($fh, @list) = @_;
  my $line = join($ODLM, @list);
  &writeln($fh, $line);
}

sub writeln($$) {
  my ($fh, $line) = @_;
  print $fh "$line\n";
}
