package.path = package.path
..";/data/pktgen-21.02.0/?.lua;/data/pktgen-21.02.0/test/?.lua;/data/pktgen-21.02.0/app/?.lua;/data/pktgen-21.02.0/../?.lua"

require "Pktgen";

-- define the ports in use
local sendport = "0";

-- parameters to use
local burst = 1;
local rate = 0.01;

function main()
    -- get dstmac and count from command line args

    -- set parameters
    pktgen.set(sendport, "burst", burst);
    pktgen.set(sendport, "rate", rate);
    pktgen.set(sendport, "count", os.getenv("MY_COUNT"));
	pktgen.set_mac(sendport, "dst", os.getenv("MY_DSTMAC"));

    pktgen.start(sendport);
    pktgen.delay(3000)
    -- spin in a loop till pktgen stops
    while( true ) do
        local sending = pktgen.isSending(sendport);
        if ( sending[tonumber(port)] == "n" ) then
            break;
        end
        pktgen.delay(1000)
    end
    pktgen.stop(sendport);
    pktgen.quit();
end

main();
